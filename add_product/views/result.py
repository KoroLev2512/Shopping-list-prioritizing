from add_product.models import GoodsModel, MatrixModel, UsersModel
from add_product.models.users import VoteStatuses
from django.db.models import Case, When, Count, Sum
from django.shortcuts import redirect, render
import pandas as pd
from django.db.models import Q


def result(request):
    goods = GoodsModel.objects.all().order_by('priority')
    
    if all(user.vote_status == VoteStatuses.VOTED.value for user in UsersModel.objects.all() if user.name != 'Семья'):
        if GoodsModel.objects.all().first().priority == 0:
            update_priorities()

        data = {'goods_priorities': [(i+1, good.name, good.priority) for i, good in enumerate(goods)]}
    else:
        data = {
            'not_voted_users': UsersModel.objects.exclude(
                Q(vote_status=VoteStatuses.VOTED.value) | Q(name="Семья")
            ).values_list('name', flat=True)
        }

    return render(request, 'result.html', data)


def update_priorities():
    users_data = count_user_weight_coeff()
    goods_data = matrix_row_sum()

    C3_sum = 0
    for good in goods_data:
        good = goods_data[good]
        weight_coeff = users_data[good['user']]['weight_coeff']
        good_votes_sum = good['sum_value']
        C3 = weight_coeff * good_votes_sum
        good.update({'C3': C3})
        C3_sum += C3
    
    [[goods_data[good].update({'norm': goods_data[good]['C3'] / C3_sum}) for good in goods_data]]

    df = pd.DataFrame.from_dict(goods_data, orient='index')

    df['rank'] = df['norm'].rank(method='average', ascending=False)
    
    for item, values in df.to_dict(orient='index').items():
        GoodsModel.objects.filter(name=item).update(priority=int(values['rank']))
    
    return


def count_user_weight_coeff():
    user_data = list(GoodsModel.objects.values('user__name').annotate(
        goods_count=Count('id')
    ).order_by('goods_count'))

    all_users = list(UsersModel.objects.all().values_list('name', flat=True))

    users_with_goods = {item['user__name'] for item in user_data}
    for user in all_users:
        if user not in users_with_goods:
            user_data.append({'user__name': user, 'goods_count': 0})
        
    user_data.sort(key=lambda x: x['goods_count'])

    goods_num = 0
    priority = 2
    priority_coeff = 1
    for user in user_data:
        if user['user__name'] == 'Семья':
            user['priority'] = 1
            continue 
        elif user['goods_count'] == goods_num:
            user['priority'] = priority
        else:
            priority += 1
            user['priority'] = priority
            goods_num = user['goods_count']
        priority_coeff += priority

    for user in user_data:
        user['weight_coeff'] = (1 - (user['priority']/priority_coeff)) / (len(user_data) - 1)
    
    user_data = {item['user__name']: {k: v for k, v in item.items() if k != 'user__name'} for item in user_data}

    return user_data


def matrix_row_sum():
    goods = GoodsModel.objects.all()

    goods_data = {}
    for good in goods:
        sum_value = MatrixModel.objects.filter(x_coordinate=good).aggregate(sum_value=Sum('value'))['sum_value'] + 3
        goods_data[good.name] = {'user': good.user.name, 'sum_value': sum_value}

    return goods_data

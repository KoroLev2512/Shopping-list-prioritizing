import random

from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import render, redirect

from add_product.models import GoodsModel, UsersModel, PairModel, MatrixModel
from add_product.models.users import VoteStatuses
from ..forms import GoodForm


def voting(request, user_id):
    if not PairModel.objects.all():
        create_all_pairs()
    if not UsersModel.objects.filter(pk=user_id).exists():
        return redirect('404notfound')
    user = UsersModel.objects.filter(pk=user_id).first()
    if not user:
        redirect('404notfound')
    data = {"name": user.name, "user_id": user_id}
    if user.vote_status == VoteStatuses.VOTED.value:
        return render(request, "golosovanie.html", context=data)

    if request.method == 'POST':
        result = request.POST.get('result')
        if result is not None:
            pair = PairModel.objects.filter(id=user.last_vote_pair).first()
            
            if update_matrix(pair, result):
            # Increase last_vote_pair
                user.last_vote_pair += 1
                
                # Check if the new last_vote_pair is valid
                if user.last_vote_pair > PairModel.objects.count():
                    user.vote_status = VoteStatuses.VOTED.value
                
                user.save()
    
    pair = PairModel.objects.filter(id=user.last_vote_pair).first()
    if pair:
        item1_name = GoodsModel.objects.filter(id=pair.good1_id).values_list('name', flat=True).first()
        item2_name = GoodsModel.objects.filter(id=pair.good2_id).values_list('name', flat=True).first()
        data.update({"item1": item1_name, "item2": item2_name})
    
    return render(request, "golosovanie.html", context=data)


def create_all_pairs():
    goods = list(GoodsModel.objects.all())
    pairs = [(goods[i], goods[j]) for i in range(len(goods)) for j in range(i + 1, len(goods))]
    random.shuffle(pairs)
    for good1, good2 in pairs:
        PairModel.objects.create(good1=good1, good2=good2)


def update_matrix(pair, result):
    if not pair:
        return False
    good1 = GoodsModel.objects.filter(id=pair.good1_id).first()
    good2 = GoodsModel.objects.filter(id=pair.good2_id).first()

    if good1 and good2:

        matrix1, created1 = MatrixModel.objects.get_or_create(
            x_coordinate=good1, y_coordinate=good2
        )

        matrix2, created2 = MatrixModel.objects.get_or_create(
            x_coordinate=good2, y_coordinate=good1
        )

        if result == '1':
            matrix1.value += 1
        if result == '2':
            matrix2.value += 1
        
        matrix1.save()
        matrix2.save()

        return True
    return False

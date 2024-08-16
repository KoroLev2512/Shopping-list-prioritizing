from django.http import JsonResponse
from django.shortcuts import render
from ..forms import GoodForm
from django.db.models import Q
from add_product.models.users import VoteStatuses

from add_product.models import GoodsModel, UsersModel


def home(request):
    data = {}
    if request.method == 'POST':
        if request.POST.get('empty_cart'):
            GoodsModel.objects.all().delete()
        else:
            item = request.POST.get('item')
            item_name, item_user = item.split(' - ')
            try:
                item = GoodsModel.objects.get(name=item_name, user=UsersModel.objects.get(name=item_user))
                item.delete()
            except GoodsModel.DoesNotExist:
                data.update({'error': "Товара не существует"})

    userform = GoodForm()
    data.update(
        {
        "form": userform,
        "users": [(user["id"], user['name']) for user in UsersModel.objects.values("name", "id")],
        "goods": [f"{name['name']} - {name['user__name']}" for name in GoodsModel.objects.values("name", "user__name")],
        "not_voted_users": UsersModel.objects.exclude(
                Q(vote_status=VoteStatuses.VOTED.value) | Q(name="Семья")
            ).values_list('name', flat=True)
        }
    )

    return render(request, "home.html", context=data)

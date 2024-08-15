from django.http import JsonResponse
from django.shortcuts import render
from ..forms import GoodForm

from add_product.models import GoodsModel, UsersModel


def home(request):
    default_users()
    if request.method == 'POST':
        item = request.POST.get('item')
        item_name, item_user = item.split(' - ')
        try:
            item = GoodsModel.objects.get(name=item_name, user=UsersModel.objects.get(name=item_user))
            item.delete()
        except GoodsModel.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Товар не найден'}, status=404)

    userform = GoodForm()
    data = {
        "form": userform,
        "users": [name['name'] for name in UsersModel.objects.values("name")],
        "goods": [f"{name['name']} - {name['user__name']}" for name in GoodsModel.objects.values("name", "user__name")]
        }
    return render(request, "home.html", context=data)


def default_users():
    a = UsersModel.objects.all()
    a.get_or_create(name='Мама')
    a.get_or_create(name='Папа')
    a.get_or_create(name='Сын')
    a.get_or_create(name='Семья')
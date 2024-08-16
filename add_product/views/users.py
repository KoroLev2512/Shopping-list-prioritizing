from django.shortcuts import render, redirect
from ..forms import GoodForm
from add_product.models import GoodsModel, UsersModel


def user(request, name):
    if request.method == 'POST':
        form = GoodForm(request.POST)
        if form.is_valid():
            good = form.save(commit=False)
            good.user = UsersModel.objects.get(name=name)
            good.save()
    userform = GoodForm()
    data = {"name": name, 
            "users": ['Мама', 'Папа', 'Сын', ], 
            "form": userform,
            "goods": [good["name"] for good in GoodsModel.objects.filter(user__name=name).values("name")],
    }
    return render(request, "user.html", context=data)


def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username and not UsersModel.objects.filter(name=username).exists():
            UsersModel.objects.create(name=username)
    data = {
        "users": [name['name'] for name in UsersModel.objects.values("name")],
    }
    return render(request, "add_user.html", data)


def delete_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        UsersModel.objects.get(name=username).delete()
    return redirect('home')
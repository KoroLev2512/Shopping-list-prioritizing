from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import render, redirect
from .forms import GoodForm
import pandas as pd
import numpy as np
from add_product.models import GoodsModel, UsersModel

# df = pd.DataFrame()
# df['name'] = ['товар1', 'товар2','товар3','товар4','товар5']
# df['family'] = ['семья', 'семья', 'папа', 'мама', 'сын']

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

def user(request, name):
    if request.method == 'POST':
        form = GoodForm(request.POST)
        good = form.save(commit=False)
        if form.is_valid() and not GoodsModel.objects.filter(name=good.name).exists():
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

    # product = request.GET.get("product", "") # Параметр строки запроса
    # # http://127.0.0.1:8000/products/mother?product=good
    # # http://127.0.0.1:8000/products/mother?product=sugar
    # if product in product_base:
    #     return HttpResponse(f"""mother
    #     <p>Имя: {name}</p>
    #     <p>Товар: {product}</p> 
    #     <p>Товар: {product_base}</p> 
    #     """)
    # else:
    #     return HttpResponseRedirect("/") # Не забыть отключить кэш

def family2(request, path, name):
    return render(request, "family.html")
    # product = request.GET.get("product", "") # Параметр строки запроса

    # return HttpResponse(f"""family
    # <p>Имя: {name}</p>
    # """)

def voting(request, name="family"):
    data = {"name": name}
    return render(request, "golosovanie.html", context=data)
    # return HttpResponse(f"""Voting
    # <p>Имя: {name}</p>
    # """)

def result(request):
    return render(request, "result.html")

# Перенаправление
# return HttpResponseRedirect("/about")
# return HttpResponsePermanentRedirect("/")
# return JsonResponse({"name": "Tom", "age": 38})

# куки
# response = HttpResponse(f"Hello {username}")
# передаем его в куки
# response.set_cookie("username", username)
# return response

# username = request.COOKIES["username"]


def to_matrix(request):
    # Высчитываем основание для деления
    Base = df['family'].value_counts()['мама'] + df['family'].value_counts()['папа'] + df['family'].value_counts()['сын'] + 1 # сумма товаров 

    # Считаем коэффициенты
    k_mother = 1 - (df['family'].value_counts()['мама'] / Base)
    k_father = 1 - (df['family'].value_counts()['папа'] / Base)
    k_son = 1 - (df['family'].value_counts()['сын'] / Base)
    k_family = 1 - (1 / Base)
    cheker = k_family + k_father + k_mother + k_son
    k_mother = k_mother / cheker
    k_father = k_father / cheker
    k_son = k_son / cheker
    k_family = k_family / cheker
    def label_koef(row):
        if row['family'] == 'мама':
            return k_mother
        if row["family"] == 'папа':
            return k_father
        if row['family'] == 'сын':
            return k_son
        return k_family
    df['koef'] = df.apply(label_koef, axis=1)
    return df['koef']

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

def default_users():
    a = UsersModel.objects.all()
    a.get_or_create(name='Мама')
    a.get_or_create(name='Папа')
    a.get_or_create(name='Сын')
    a.get_or_create(name='Семья')
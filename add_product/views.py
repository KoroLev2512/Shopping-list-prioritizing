from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import render
from .forms import UserForm
import pandas as pd
import numpy as np

df = pd.DataFrame()
df['name'] = ['товар1', 'товар2','товар3','товар4','товар5']
df['family'] = ['семья', 'семья', 'папа', 'мама', 'сын']

def index(request):
    userform = UserForm()
    data = {"form": userform}
    return render(request, "index.html", context=data)


def mother(request, name):
    return render(request, "mama.html")
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

def father(request, name):
    return render(request, "papa.html")
    # return render(request, "index.html")
    # product = request.GET.get("product", "") # Параметр строки запроса

    # return HttpResponse(f"""father
    # <p>Имя: {name}</p>
    # """)

def son(request, name):
    return render(request, "son.html")
    # product = request.GET.get("product", "") # Параметр строки запроса

    # return HttpResponse(f"""son
    # <p>Имя: {name}</p>
    # """)
def family(request, name):
    return render(request, "family.html")

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
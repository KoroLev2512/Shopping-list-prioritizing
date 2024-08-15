from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import render, redirect
from ..forms import GoodForm
import pandas as pd
import numpy as np
from add_product.models import GoodsModel, UsersModel

def voting(request, name="family"):
    data = {"name": name}
    return render(request, "golosovanie.html", context=data)
    # return HttpResponse(f"""Voting
    # <p>Имя: {name}</p>
    # """)



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
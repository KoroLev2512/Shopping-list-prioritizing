import random
import pandas as pd
import numpy as np

from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import render, redirect

from add_product.models import GoodsModel, UsersModel, PairModel, MatrixModel
from add_product.models.users import VoteStatuses
from ..forms import GoodForm


def update_matrix(pair):
    if not pair:
        return False
    good1 = GoodsModel.objects.filter(id=pair.good1_id).first()
    good2 = GoodsModel.objects.filter(id=pair.good2_id).first()

    if good1 and good2:

        matrix1, created1 = MatrixModel.objects.get_or_create(
            x_coord=good1, y_coord=good2
        )

        matrix2, created2 = MatrixModel.objects.get_or_create(
            x_coord=good2, y_coord=good1
        )

        if result == '1':
            matrix1.value += 1
        if result == '2':
            matrix2.value += 1
        
        matrix1.save()
        matrix2.save()


def voting(request, name):
    if not PairModel.objects.all():
        create_all_pairs()
    data = {"name": name}
    user = UsersModel.objects.filter(name=name).first()
    if user.vote_status == VoteStatuses.VOTED.value:
        return render(request, "golosovanie.html", context=data)

    if request.method == 'POST':
        result = request.POST.get('result')
        if result is not None:
            pair = PairModel.objects.filter(id=user.last_vote_pair).first()
            
            if update_matrix(pair):
                
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


def create_all_pairs():
    goods = list(GoodsModel.objects.all())
    pairs = [(goods[i], goods[j]) for i in range(len(goods)) for j in range(i + 1, len(goods))]
    random.shuffle(pairs)
    for good1, good2 in pairs:
        PairModel.objects.create(good1=good1, good2=good2)
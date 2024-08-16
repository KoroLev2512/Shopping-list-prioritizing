from django.http import JsonResponse
from django.shortcuts import render, redirect
from ..forms import GoodForm
from django.db.models import Q
from add_product.models.users import VoteStatuses

from add_product.models import GoodsModel, UsersModel


def notfound(request):
    return render(request, "404.html")

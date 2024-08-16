from django.db import models
from .users import UsersModel


class GoodsModel(models.Model):
    name = models.CharField(verbose_name='Товар', unique=True, max_length=255)
    user = models.ForeignKey(UsersModel, on_delete=models.CASCADE, verbose_name='Пользователь')
    priority = models.IntegerField(verbose_name='Приоритет', default=0)

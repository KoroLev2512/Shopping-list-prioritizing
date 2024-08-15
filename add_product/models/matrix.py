from django.db import models
from .goods import GoodsModel


class MatrixModel(models.Model):
    x_coordinate = models.ForeignKey(
        GoodsModel,
        on_delete=models.CASCADE,
        related_name='x_matrices',
        verbose_name='Первый товар'
    )
    y_coordinate = models.ForeignKey(
        GoodsModel,
        on_delete=models.CASCADE,
        related_name='y_matrices',
        verbose_name='Второй товар'
    )
    value = models.IntegerField(verbose_name="Результат голосования")

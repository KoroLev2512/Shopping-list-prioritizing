import random

from django.db import models
from . import GoodsModel
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class PairModel(models.Model):
    id = models.AutoField(primary_key=True)
    good1 = models.ForeignKey(GoodsModel, related_name='good1_pairs', on_delete=models.CASCADE)
    good2 = models.ForeignKey(GoodsModel, related_name='good2_pairs', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.id is None:
            latest_id = PairModel.objects.aggregate(models.Max('id'))['id__max']
            self.id = latest_id + 1 if latest_id is not None else 1
        super().save(*args, **kwargs)

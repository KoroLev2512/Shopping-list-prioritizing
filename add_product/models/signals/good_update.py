from .. import GoodsModel, UsersModel, PairModel
from ..users import VoteStatuses
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=GoodsModel)
@receiver(post_delete, sender=GoodsModel)
def update_pairs(sender, instance, **kwargs):
    UsersModel.objects.update(
        last_vote_pair=1, 
        vote_status=VoteStatuses.NOT_VOTED.value
    )

@receiver(post_save, sender=GoodsModel)
@receiver(post_delete, sender=GoodsModel)
def update_pairs(sender, instance, **kwargs):
    PairModel.objects.all().delete()

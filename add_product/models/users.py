from django.db import models
from enum import Enum

class VoteStatuses(Enum):
    NOT_VOTED = 'not_voted'
    VOTED = 'voted'


class UsersModel(models.Model):
    name = models.CharField(verbose_name='Имя', unique=True, max_length=255)
    last_vote_pair = models.IntegerField(verbose_name="Пара для голосования", default=1)
    vote_status = models.CharField(
        verbose_name='Статус голосования',
        max_length=50,
        default= VoteStatuses.NOT_VOTED.value,
        choices=[(status.name, status.value) for status in VoteStatuses]
    )

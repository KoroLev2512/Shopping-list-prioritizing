from django.db import models
from enum import Enum


class VoteStatuses(Enum):
    NOT_VOTED = 'not_voted'
    VOTED = 'voted'


class UsersModel(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=255)
    vote_status = models.CharField(
        verbose_name='Статус голосования',
        max_length=50,
        choices=[(role.name, role.value) for role in VoteStatuses]
    )
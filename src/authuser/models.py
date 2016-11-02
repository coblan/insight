# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User,Group
from django.db import models

class PermitModel(models.Model):
    group = models.ForeignKey(Group,verbose_name='group')
    model = models.CharField('model',default='')
    permit = models.JSONField()
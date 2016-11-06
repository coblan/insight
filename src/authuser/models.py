# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User,Group
from django.db import models

# class PermitModel(models.Model):
    # group = models.ForeignKey(Group,verbose_name='group')
    # model = models.CharField('model',default='')
    # permit = models.TextField(verbose_name='permit',default='')\


class LogModel(models.Model):
    at = models.DateTimeField(auto_now=True)
    user= models.ForeignKey(User,verbose_name='操作者')
    key =models.CharField('key',max_length=200)
    op = models.CharField('操作类型',max_length=100)
    detail =models.TextField('细节',blank=True)
    

# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class BasicInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField('姓名', max_length=50, blank=True)
    age = models.CharField('年龄', max_length=50, blank=True)
    
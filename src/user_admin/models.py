# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class BasicInfo(models.Model):
    # , on_delete=models.SET_NULL
    user = models.OneToOneField(User, blank=True, null=True)
    name = models.CharField('姓名', max_length=50, blank=True)
    age = models.CharField('年龄', max_length=50, blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        permissions = (('read_basicinfo','At leaset read the records'),
                       )

class MM(models.Model):
    info = models.ManyToManyField(BasicInfo,verbose_name='jjyy')
    name = models.CharField('姓名', max_length=50, blank=True)
    
    def __unicode__(self):
        return self.name

class Fore(models.Model):
    info = models.ForeignKey(BasicInfo,verbose_name='jjyy')
    name = models.CharField('姓名', max_length=50, blank=True)
    
    def __unicode__(self):
        return self.name    
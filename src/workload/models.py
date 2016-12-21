# encoding:utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class TaskModel(models.Model):
    name=models.CharField('名称',max_length=300,blank=True)
    parent=models.ForeignKey('self',verbose_name='父工作',null=True,blank=True)
    owner=models.ForeignKey(User,verbose_name='从属于',null=True,blank=True)
    desp= models.TextField('详细介绍',blank=True)
    
    def __unicode__(self):
        return self.name

class WorkModel(models.Model):
    task=models.ForeignKey(TaskModel,verbose_name='所属任务',null=True,blank=True)
    worker=models.ForeignKey(User,verbose_name='worker',null=True,blank=True)
    quality=models.CharField('质量',max_length=100,blank=True)
    quantity=models.CharField('工作量',max_length=100,blank=True)
    creative=models.CharField('创新性',max_length=100,blank=True)
    update_date=models.DateTimeField(verbose_name='更新日期',auto_now=True)
    manager=models.ForeignKey(User,verbose_name='管理者',null=True,blank=True,related_name='managed_works')
    short_desp=models.CharField('工作简介',max_length=200,blank=True)
    long_desp=models.TextField('详细介绍',blank=True)
    
    def __unicode__(self):
        return unicode(self.task) + '_' + str(self.worker)
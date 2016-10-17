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

class EmployeeInfo(models.Model):
    baseinfo=models.OneToOneField(BasicInfo,blank=True,null=True)
    employ_id = models.CharField('职员ID',max_length=50,blank=True)
    position = models.CharField('职位',max_length=100,blank=True)
    salary_level = models.FloatField('工资',max_length=100,blank=True)


class SalaryRecords(models.Model):
    empoyee=models.ForeignKey(EmployeeInfo,verbose_name='员工',blank=True,null=True)
    base_salary = models.FloatField('基本工资',blank=True)
    merit_pay = models.FloatField('绩效工资',blank=True)
    allowance = models.FloatField('补贴',blank=True)
    social_security = models.FloatField('社保',blank=True)
    reserved_funds = models.FloatField('社保',blank=True)
    month = models.ForeignKey('Month',verbose_name='月份',blank=True,null=True)
    adapt_day=models.FloatField('修正',blank=True)

class Month(models.Model):
    workdays = models.FloatField('应该工作天数',blank=True)
    
    

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
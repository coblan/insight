# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User,Group
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
    baseinfo=models.OneToOneField(BasicInfo,blank=True,null=True,on_delete=models.SET_NULL)
    employ_id = models.CharField('职员ID',max_length=50,blank=True)
    position = models.CharField('职位',max_length=100,blank=True)
    salary_level = models.FloatField('工资',max_length=100,blank=True,null=True)
    
    def __unicode__(self):
        if self.baseinfo:
            return self.baseinfo.name
        else:
            return self.employ_id
    
    class Meta:
        verbose_name='员工信息'

class SalaryRecords(models.Model):
    empoyee=models.ForeignKey(EmployeeInfo,verbose_name='员工',blank=True,null=True)
    base_salary = models.FloatField('基本工资',blank=True,null=True)
    merit_pay = models.FloatField('绩效工资',blank=True,null=True)
    allowance = models.FloatField('补贴',blank=True,null=True)
    social_security = models.FloatField('社保',blank=True,null=True)
    reserved_funds = models.FloatField('公积金',blank=True,null=True)
    month = models.ForeignKey('Month',verbose_name='月份',blank=True,null=True)
    adapt_day=models.FloatField('修正天数',blank=True,null=True)
    
    def __unicode__(self):
        try:
            return '{employee} 的工资'.format(employee=self.empoyee.baseinfo.name)
        except AttributeError:
            return '某人工资'
    

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
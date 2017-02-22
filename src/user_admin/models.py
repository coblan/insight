# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User,Group
from django.db import models
from django.utils.translation import ugettext as _

    


class EmployeeModel(models.Model):
    user = models.ForeignKey(User,verbose_name=_('user'), blank=True, null=True)
    baseinfo=models.OneToOneField('BasicInfo',verbose_name='基本信息',blank=True,null=True,on_delete=models.SET_NULL)
    employ_id = models.CharField('职员ID',max_length=50,unique=True)
    position = models.CharField('职位',max_length=100,blank=True)
    salary_level = models.FloatField('工资',max_length=100,blank=True,null=True)
    
    def __unicode__(self):
        if self.baseinfo:
            return self.baseinfo.name
        else:
            return self.employ_id
    
    class Meta:
        verbose_name='工作信息'

# Create your models here.
class BasicInfo(models.Model):
    # , on_delete=models.SET_NULL
    name = models.CharField(_('name'), max_length=50, blank=True)
    age = models.CharField(_('age'), max_length=50, blank=True)
    head = models.CharField('head image',max_length=200,blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name='基本信息'
        permissions = (('read_basicinfo','At leaset read the records'),
                       )


class SalaryRecords(models.Model):
    empoyee=models.ForeignKey(EmployeeModel,verbose_name='员工',blank=True,null=True)
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
    
    class Meta:
        verbose_name='工资记录'    
    

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
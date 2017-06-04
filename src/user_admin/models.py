# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User,Group
from django.db import models
from django.utils.translation import ugettext as _
from helpers.common.employee import Employee
from helpers.common.human import HumanInfo
from helpers.common.department import DepartmentBase

class EmployeeModel(Employee):
    #user = models.ForeignKey(User,verbose_name=_('user'), blank=True, null=True)
    baseinfo=models.OneToOneField('BasicInfo',verbose_name=_('basic info'),blank=True,null=True,on_delete=models.SET_NULL)
    #employ_id = models.CharField(_('Employee ID'),max_length=50,unique=True)
    position = models.CharField(_('job position'),max_length=100,blank=True)
    salary_level = models.FloatField(_('salary level'),max_length=100,blank=True,null=True)
    
    #def __unicode__(self):
        #if self.baseinfo:
            #return self.baseinfo.name
        #else:
            #return self.employ_id
    
    class Meta:
        verbose_name=_('Employee Info')

# Create your models here.
class BasicInfo(HumanInfo):
    # , on_delete=models.SET_NULL
    #name = models.CharField(_('name'), max_length=50, blank=True)
    #age = models.CharField(_('age'), max_length=50, blank=True)
    #head = models.CharField(_('head image'),max_length=200,blank=True)
    #id_number=models.CharField(_('id  number'),max_length=200,blank=True)
    #address=models.CharField(_('address'),max_length=500,blank=True)
    #gen = models.CharField(_('gen'),max_length=30,blank=True)
    #phone = models.CharField(_('phone'),max_length=100,blank=True)
    
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name=_('basic info')
        #permissions = (('read_basicinfo','At leaset read the records'),
                       #)


class SalaryRecords(models.Model):
    empoyee=models.ForeignKey(EmployeeModel,verbose_name=_('employee'),blank=True,null=True)
    base_salary = models.FloatField(_('basic salary'),blank=True,null=True)
    merit_pay = models.FloatField(_('merit pay'),blank=True,null=True)
    allowance = models.FloatField('补贴',blank=True,null=True)
    social_security = models.FloatField('社保',blank=True,null=True)
    reserved_funds = models.FloatField('公积金',blank=True,null=True)
    # month = models.ForeignKey('Month',verbose_name='月份',blank=True,null=True)
    month=models.CharField(_('month'),max_length=50,blank=True)
    adapt_day=models.FloatField('修正天数',blank=True,null=True)
    is_checked=models.BooleanField(_('is make sure'),default=False)
    
    def __unicode__(self):
        try:
            return _('salary of %(employee)s')%{'employee':self.empoyee.baseinfo.name}
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
    

class Department(models.Model):
    name =models.CharField(_('department name'),max_length=300)
    label =models.CharField(_('department label'),max_length=300,blank=True)
    detail=models.TextField(verbose_name=_('detail'),blank=True)
    par = models.ForeignKey('Department',verbose_name=_('parent department'),blank=True,null=True,related_name='sub_dep')
    #sub_depart=models.CharField(_('sub department'),max_length=500,blank=True)
    
    def __unicode__(self):
        return self.label
    
class Department2(DepartmentBase):
    pass


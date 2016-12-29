# encoding:utf-8
from __future__ import unicode_literals

from helpers.director.model_admin.permit import Permit
from user_admin.models import SalaryRecords,BasicInfo,EmployeeModel,User,Group
from workload.models import WorkModel,TaskModel
from helpers.director.model_admin.render import render_dc
from django.core.urlresolvers import reverse
#from django.urls import reverse

def can_touch(model):
    def _func(user):
        validator = Permit(model, user)
        return validator.can_access()
    return _func

def page(name):
    return reverse('model_table',kwargs={'name':name})

#menus=[
    #{'name':'hello','label':'hello','url':'/hello/','icon':'<i class="fa fa-home" aria-hidden="true"></i>'},
    #{'name':'basice','label':'用户相关','url':'/hello/model/basicinfo/','icon':'<i class="fa fa-users" aria-hidden="true"></i>',
     #'submenu':[{'name':'basice','label':'basicinfo','url':'/hello/model/basicinfo/','invalid':cant_touch(BasicInfo)},
                #{'name':'user','label':'用户管理','url':'/hello/model/user/','invalid':cant_touch(User)},
                #{'name':'group','label':'用户组','url':'/hello/model/group/','invalid':cant_touch(Group)},
                #{'name':'employee_set','label':'employee','url':'/hello/model/employee_set/','invalid':cant_touch(Group)},
                #]},
    #{'name':'employee','label':'雇员管理','url':'/hello/model/employee_prod/','icon':'<i class="fa fa-users" aria-hidden="true"></i>',
     #'submenu':[{'name':'employee_prod','label':'员工信息管理','url':'/hello/model/employee_prod/','invalid':cant_touch(EmployeeInfo)},
                #{'name':'salary_records','label':'工资记录','url':'/hello/model/salary_records/','invalid': cant_touch(SalaryRecords) }]}
#]
  
menus=[
    {'name':'hello','label':'home','url':'/hello/','icon':'<i class="fa fa-home" aria-hidden="true"></i>'},
    {'name':'basice','label':'账号管理','url':lambda: reverse('model_table',kwargs={'name':'user'}),'icon':'<i class="fa fa-users" aria-hidden="true"></i>',
     'submenu':[
                {'name':'user','label':'用户管理','url':lambda: page('user'),'visible':can_touch(User)},
                {'name':'group','label':'用户组','url':lambda:page('group'),'visible':can_touch(Group)},
                ]},
    {'name':'employee','label':'员工管理','url':lambda: reverse('model_table',kwargs={'name':'basicinfo'}),'icon':'<i class="fa fa-users" aria-hidden="true"></i>',
     'submenu':[
         {'name':'basice','label':'人员信息','url':lambda: reverse('model_table',kwargs={'name':'basicinfo'}),'visible':can_touch(BasicInfo)},    
         {'name':'employee_set','label':'员工名册','url':lambda: reverse('model_table',kwargs={'name':'employee'}),'visible':can_touch(EmployeeModel)},
        
         ]},
    {'name':'workload','label':'工作量统计','url':lambda: reverse('model_table',kwargs={'name':'workloads'}),'icon':'<i class="fa fa-users" aria-hidden="true"></i>',
     'submenu':[{'name':'task','label':'任务','url':lambda: reverse('model_table',kwargs={'name':'task'}),'visible':can_touch(TaskModel)},
                {'name':'workload','label':'工作','url':lambda: reverse('model_table',kwargs={'name':'workloads'}),'visible':can_touch(WorkModel)}
                ]
     }

]

render_dc['menu']=menus
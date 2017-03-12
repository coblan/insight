# encoding:utf-8
from __future__ import unicode_literals

from helpers.director.model_admin.permit import Permit
from user_admin.models import SalaryRecords,BasicInfo,EmployeeModel,User,Group
from workload.models import WorkModel,TaskModel
from helpers.director.model_admin.render import render_dc
from django.core.urlresolvers import reverse

from helpers.pageadaptor.models import WebPage

def can_touch(model):
    def _func(user):
        validator = Permit(model, user)
        return validator.can_access()
    return _func

def can_list(ls):
    def _func(user):
        for model in ls:
            validator = Permit(model, user)
            if validator.can_access():
                return True
    return _func    

def page(name):
    return lambda: reverse('model_table',kwargs={'name':name})

def fa(name):
    return '<i class="fa %s" aria-hidden="true"></i>'%name

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
    {'label':'home','url':'/','icon':fa('fa-home')},
    {'label':'账号管理','url':page('user'),'icon':fa('fa-users'),'visible':can_list((User,Group)),
     'submenu':[
                {'label':'用户管理','url':page('user'),'visible':can_touch(User)},
                {'label':'用户组','url':page('group'),'visible':can_touch(Group)},
                ]},
    {'label':'员工管理','icon':fa('fa-users'),'visible':can_list((BasicInfo,EmployeeModel,SalaryRecords)),
     'submenu':[
         #{'label':'人员信息','url':page('basicinfo'),'visible':can_touch(BasicInfo)},    
         {'label':'员工名册','url':page('employee'),'visible':can_touch(EmployeeModel)},
        {'label':'工资记录','url':page('salary'),'visible':can_touch(SalaryRecords)},
         ]},
    {'label':'工作量统计','icon':fa('fa-users'),'visible':can_list((TaskModel,WorkModel)),
     'submenu':[{'label':'任务','url': page('task'),'visible':can_touch(TaskModel)},
                {'label':'工作','url':page('workloads'),'visible':can_touch(WorkModel)}
                ]
     },
    {'label':'Page Admin','url':page('webpage'),'icon':fa('fa-home'),'visible':can_touch(WebPage)},

]

render_dc['menu']=menus
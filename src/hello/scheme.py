# encoding:utf-8
from __future__ import unicode_literals

from core.model_render import Permit
from user_admin.models import SalaryRecords,BasicInfo,EmployeeInfo,User,Group

def cant_touch(model):
    def _func(user):
        validator = Permit(model, user)
        return not validator.can_touch()
    return _func


menus=[
    {'name':'hello','label':'hello','url':'/hello/','icon':'<i class="fa fa-home" aria-hidden="true"></i>'},
    {'name':'basice','label':'用户相关','url':'/hello/model/basicinfo/','icon':'<i class="fa fa-users" aria-hidden="true"></i>',
     'submenu':[{'name':'basice','label':'basicinfo','url':'/hello/model/basicinfo/','invalid':cant_touch(BasicInfo)},
                {'name':'user','label':'用户管理','url':'/hello/model/user/','invalid':cant_touch(User)},
                {'name':'group','label':'用户组','url':'/hello/model/group/','invalid':cant_touch(Group)},
                {'name':'employee_set','label':'employee','url':'/hello/model/employee_set/','invalid':cant_touch(Group)},
                ]},
    {'name':'employee','label':'雇员管理','url':'/hello/model/employee_prod/','icon':'<i class="fa fa-users" aria-hidden="true"></i>',
     'submenu':[{'name':'employee_prod','label':'员工信息管理','url':'/hello/model/employee_prod/','invalid':cant_touch(EmployeeInfo)},
                {'name':'salary_records','label':'工资记录','url':'/hello/model/salary_records/','invalid': cant_touch(SalaryRecords) }]}
]
  

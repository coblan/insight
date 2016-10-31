# encoding:utf-8
from __future__ import unicode_literals

menus=[
    {'name':'hello','label':'hello','url':'/hello/','icon':'<i class="fa fa-home" aria-hidden="true"></i>'},
    {'name':'basice','label':'用户相关','url':'/hello/model/basicinfo/','icon':'<i class="fa fa-users" aria-hidden="true"></i>',
     'submenu':[{'name':'basice','label':'basicinfo','url':'/hello/model/basicinfo/','valid':lambda user:user.has_perm('user_admin.read_basicinfo')},
                {'name':'user','label':'用户管理','url':'/hello/model/user/'},
                {'name':'group','label':'用户组','url':'/hello/model/group/'},
                {'name':'employee_set','label':'employee','url':'/hello/model/employee_set/'},
                ]},
    {'name':'employee','label':'雇员管理','url':'/hello/model/employee_prod/','icon':'<i class="fa fa-users" aria-hidden="true"></i>',
     'submenu':[{'name':'employee_prod','label':'员工信息管理','url':'/hello/model/employee_prod/'},
                {'name':'salary_records','label':'工资记录','url':'/hello/model/salary_records/'}]}
]
  

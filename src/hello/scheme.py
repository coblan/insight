# encoding:utf-8
from __future__ import unicode_literals

menus=[
    {'name':'hello','label':'hello','url':'/hello/','icon':'<i class="fa fa-home" aria-hidden="true"></i>'},
    {'name':'basice','label':'user','url':'/hello/model/basicinfo/','icon':'<i class="fa fa-users" aria-hidden="true"></i>',
     'submenu':[{'name':'basice','label':'basicinfo','url':'/hello/model/basicinfo/','valid':lambda user:user.has_perm('user_admin.read_basicinfo')},
                {'name':'user','label':'user admin','url':'/hello/model/user/'},
                {'name':'group','label':'User Group','url':'/hello/model/group/'},
                {'name':'employee_set','label':'employee','url':'/hello/model/employee_set/'},
                {'name':'employee_prod','label':'员工信息管理','url':'/hello/model/employee_prod/'}]}
]
  

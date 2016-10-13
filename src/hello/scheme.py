menus=[
    {'name':'hello','label':'hello','url':'/hello/','icon':'<i class="fa fa-home" aria-hidden="true"></i>'},
    {'name':'basice','label':'user','url':'/hello/model/basicinfo/','icon':'<i class="fa fa-users" aria-hidden="true"></i>',
     'submenu':[{'name':'basice','label':'basicinfo','url':'/hello/model/basicinfo/','valid':lambda user:user.has_perm('user_admin.read_basicinfo')},
                {'name':'user','label':'user admin','url':'/hello/model/user/'},
                {'name':'group','label':'User Group','url':'/hello/model/group/'}]}
]
  

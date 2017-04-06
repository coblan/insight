# encoding:utf-8

"""
试着加入新的engine，对页面请求进行路由
"""
from user_admin.models import SalaryRecords,BasicInfo,EmployeeModel,User,Group,Department
from workload.models import WorkModel,TaskModel
from helpers.director.engine import BaseEngine,can_list,can_touch,fa,page
from helpers.pageadaptor.models import WebPage
from helpers.director.admin import UserFormPage,UserTablePage,GroupFormPage,GroupTablePage

class InsightEngine(BaseEngine):
    menu=[
        {'label':'home','url':'/','icon':fa('fa-home')},
        {'label':'账号管理','url':page('user'),'icon':fa('fa-users'),'visible':can_list((User,Group)),
         'submenu':[
                    {'label':'用户管理','url':page('user'),'visible':can_touch(User)},
                    {'label':'用户组','url':page('group'),'visible':can_touch(Group)},
                    ]},
        {'label':'组织管理','icon':fa('fa-users'),'visible':can_list((BasicInfo,EmployeeModel,SalaryRecords)),
         'submenu':[
             {'label':'部门管理','url':page('department'),'visible':can_touch(Department)},    
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

# InsightEngine.add_pages({'user':UserTablePage,
                         # 'user.edit':UserFormPage,
                         # 'group':GroupTablePage,
                         # 'group.edit':GroupFormPage})
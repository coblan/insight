# encoding:utf-8

"""
试着加入新的engine，对页面请求进行路由
"""
from user_admin.models import SalaryRecords,BasicInfo,EmployeeModel,User,Group,Department,Department2
from workload.models import WorkModel,TaskModel
from helpers.director.engine import BaseEngine,can_list,can_touch,fa,page
from helpers.pageadaptor.models import WebPage
from helpers.director.admin import UserFormPage,UserTablePage,GroupFormPage,GroupTablePage
from helpers.director.shortcut import page_dc
from helpers.case.organize import menu as organize_menu

class InsightEngine(BaseEngine):
    url_name='insight'
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
             {'label':'部门管理2','url':page('department2'),'visible':can_touch(Department2)},    
             {'label':'员工名册','url':page('employee'),'visible':can_touch(EmployeeModel)},
            {'label':'工资记录','url':page('salary'),'visible':can_touch(SalaryRecords)},
            
             ]},
        organize_menu.pc_menu,
        {'label':'工作量统计','icon':fa('fa-users'),'visible':can_list((TaskModel,WorkModel)),
         'submenu':[{'label':'任务','url': page('task'),'visible':can_touch(TaskModel)},
                    {'label':'工作','url':page('workloads'),'visible':can_touch(WorkModel)}
                    ]
         },
        {'label':'Page Admin','url':page('webpage'),'icon':fa('fa-home'),'visible':can_touch(WebPage)},
    
    ]    

InsightEngine.add_pages(page_dc)

class MobileEngine(BaseEngine):
    url_name='mobile_insight'
    menu=[
        {'label':'home','url':page('m_home'),'icon':fa('fa-users fa-2x')},
        {'label':'工作量','url':page('workloads.mobile'),'icon':fa('fa-camera-retro fa-2x')},
        {'label':'员工','url':page('employee.mobile'),'icon':fa('fa-users fa-2x')},
        {'label':'工资','url':page('salary.mobile'),'icon':fa('fa-car fa-2x')},
    ]


class MHome(object):
    template='hello/m_home.html'
    need_login=False
    def __init__(self,request):
        self.request=request
    
    def get_context(self):
        return {}


MobileEngine.add_pages(page_dc)
MobileEngine.add_pages({'m_home':MHome})
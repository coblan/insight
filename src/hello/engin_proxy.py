# encoding:utf-8

"""
试着加入新的engine，对页面请求进行路由
"""
#from user_admin.models import SalaryRecords,BasicInfo,EmployeeModel,User,Group,Department,Department2
from django.contrib.auth.models import User,Group
#from workload.models import WorkModel,TaskModel
from helpers.director.engine import BaseEngine,can_list,can_touch,fa,page
from helpers.pageadaptor.models import WebPage
from helpers.director.admin import UserFormPage,UserTablePage,GroupFormPage,GroupTablePage
from helpers.director.shortcut import page_dc
from helpers.case.organize import menu as organize_menu
from helpers.case.work import menu as work_menu
from helpers.director.models import KVModel
from helpers.maintenance.update_static_timestamp import static_file_timestamp_dict
from helpers.pageadaptor.shotcut import Press
import urllib

class InsightEngine(BaseEngine):
    url_name='insight'
    menu=[
        {'label':'home','url':page('press',append='?_name=home'),'icon':fa('fa-home')},
        {'label':'账号管理','url':page('user'),'icon':fa('fa-users'),'visible':can_list((User,Group)),
         'submenu':[
                    {'label':'用户管理','url':page('user'),'visible':can_touch(User)},
                    {'label':'用户组','url':page('group'),'visible':can_touch(Group)},
                    ]},
        # {'label':'组织管理','icon':fa('fa-users'),'visible':can_list((BasicInfo,EmployeeModel,SalaryRecords)),
         # 'submenu':[
             # {'label':'部门管理','url':page('department'),'visible':can_touch(Department)},  
             # {'label':'部门管理2','url':page('department2'),'visible':can_touch(Department2)},    
             # {'label':'员工名册','url':page('employee'),'visible':can_touch(EmployeeModel)},
            # {'label':'工资记录','url':page('salary'),'visible':can_touch(SalaryRecords)},
            
             # ]},
        organize_menu.pc_menu,
        work_menu.pc_menu,
        # {'label':'工作量统计','icon':fa('fa-users'),'visible':can_list((TaskModel,WorkModel)),
         # 'submenu':[{'label':'任务','url': page('task'),'visible':can_touch(TaskModel)},
                    # {'label':'工作','url':page('workloads'),'visible':can_touch(WorkModel)}
                    # ]
         # },
        {'label':'Page Admin','url':page('webpage'),'icon':fa('fa-home'),'visible':can_touch(WebPage)},
        {'label':'设置','url':page('kv'),'icon':fa('fa-home'),'visible':can_touch(KVModel)},
    ]    

InsightEngine.add_pages(page_dc)

class MobileEngine(BaseEngine):
    url_name='mobile_insight'
    prefer='wx'
    root_page='/wx/home.wx'
    menu=organize_menu.wx_menu+ \
        work_menu.wx_menu 
    
    def custome_ctx(self, ctx):
        ctx['stamp']=static_file_timestamp_dict
        
        help_name = 'help_'+ctx['page_name']
        engine_press=Press(help_name)
        if engine_press.page:
            ctx['help_url']=self.get_url('press')+'?_name=%s'%help_name
        return ctx
    #[
        #{'label':'home','url':page('home.wx'),'icon':fa('fa-users fa-2x')},
        #{'label':'工作量','url':page('workloads.mobile'),'icon':fa('fa-camera-retro fa-2x')},
        #{'label':'员工','url':page('employee.mobile'),'icon':fa('fa-users fa-2x')},
        #{'label':'工资','url':page('salary.mobile'),'icon':fa('fa-car fa-2x')},
        #{'label':'员工名单','url':page('organize.employee.wx'),'icon':fa('fa-user-o fa-2x')},
        #{'label':'部门结构','url':page('organize.department'),'icon':fa('fa-sitemap fa-2x')}, 
        

    #]
    
    # def get_ctx(self, ctx):
        # ctx['menu_group']=[
            # {'label':'','group':[]}
        # ]


# class MHome(object):
    # template='wx/home.html'
    # need_login=False
    # def __init__(self,request):
        # self.request=request
    
    # def get_context(self):
        # return {}


MobileEngine.add_pages(page_dc)
# MobileEngine.add_pages({'m_home':MHome})

class F7Engine(BaseEngine):
    url_name='f7_engine'
    prefer='f7'
    root_page='/f7/home.f7'
    
    menu=organize_menu.wx_menu+ \
        work_menu.f7_menu     

class F7FrameWraper(object):
    template='f7/frame_wraper.html'
    def __init__(self,request):
        src= request.GET.get('src')
        self.src=urllib.unquote( src)
        
    def get_context(self):
        return {'src':self.src}
    
F7Engine.add_pages(page_dc)
F7Engine.add_pages({'f7.html':F7FrameWraper})
    

    
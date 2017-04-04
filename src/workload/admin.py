# encoding:utf-8
from __future__ import unicode_literals

from django.db.models import Q
from helpers.director.model_admin.tabel import ModelTable,RowSearch,RowFilter,RowSort
from helpers.director.model_admin.render import model_page_dc,model_dc


from helpers.director.shortcut import TablePage,FormPage
from helpers.director.model_admin.fields import ModelFields
from helpers.director.db_tools import to_dict
from helpers.director.model_admin.permit import permit_list,has_permit

from models import WorkModel,TaskModel

from hello.engin_proxy import InsightEngine

class TaskSearch(RowSearch):
    names=['name']
    model=TaskModel

class TaskField(ModelFields):
    class Meta:
        model=TaskModel
        fields=['name','parent','owner','desp']
        

class TaskTable(ModelTable):
    model=TaskModel
    search=TaskSearch
    include=['name','parent','owner']
    
    def get_rows(self):
        query=self.get_query()
        ls=[]
        for row in query:
            dc={
                'parent':str(row.parent) if row.parent else '---',
                'owner':str(row.owner) if row.owner else '---'
            }
            ls.append(to_dict(row,filt_attr=lambda x: dc,include=self.permited_fields()))
        return ls    

class TaskTablePage(TablePage):
    tableCls=TaskTable

class TaskFormPage(FormPage):
    template='workload/task_form.html'
    fieldsCls=TaskField
    
class WorkSearch(RowSearch):
    names=['worker','manager']
    model=WorkModel
    
    def get_query(self,query):
        if self.q:
            exp=Q()
            kw={}
            if 'worker' in self.valid_name:
                exp= exp | Q(worker__baseinfo__name__icontains=self.q)
            if 'manager' in self.valid_name:
                exp = exp | Q(manager__baseinfo__name__icontains=self.q)
            return query.filter(exp)
        else:
            return query    
    
class WorkloadField(ModelFields):
    class Meta:
        model=WorkModel
        fields=['task','worker','quality','quantity','creative','short_desp','long_desp','manager']
    
    def save_form(self):
        #if not self.instance.pk and self.crt_user.employeemodel_set.exists():
            #self.instance.manager=self.crt_user.employeemodel_set.first()
        rt = super(WorkloadField,self).save_form()
        return rt
    
class WorkTable(ModelTable):
    model=WorkModel
    search=WorkSearch
    include=['worker','task','quality','quantity','creative','manager','short_desp']
    def get_rows(self):
        query=self.get_query()
        ls=[]
        for row in query:
            dc={
                'worker':str(row.worker) if row.worker else '---',
                'task':str(row.task) if row.task else '---',
                'manager':str(row.manager) if row.manager else '---',
            }
            ls.append(to_dict(row,filt_attr=lambda x: dc,include=self.permited_fields()))
        return ls
        #return [to_dict(x,filt_attr=lambda x:{'worker':str(x.worker) if x.worker else '---'}, include=self.permited_fields()) for x in query]    
        
    def inn_filter(self, query):
        if has_permit(self.crt_user,'workload.view_all_task'):
            return query
        else:
            return query.filter(Q(worker__user=self.crt_user)|Q(manager__user=self.crt_user))

class WorkTablePage(TablePage):
    tableCls=WorkTable
    

class WorkFormPage(FormPage):
    fieldsCls=WorkloadField
    
# 将该fields注册为model的管理类
model_dc[WorkModel]={'fields':WorkloadField}
model_dc[TaskModel]={'fields':TaskField}

# 该字典制定了配套的table页面和form页面，利用该字典，一般在table的第一个字段会生成指向form页面的链接。
model_page_dc['workloads']={'table':WorkTablePage,'form':WorkFormPage}
model_page_dc['task']={'table':TaskTablePage,'form':TaskFormPage}


permit_list.append({'name':'workload','label':'人员负荷','fields':[
    {'name':'view_all_task','label':'查看所有负荷','type':'bool'},
    {'name':'sp2','label':'工作统计','type':'bool'}
]})

permit_list.append(WorkModel)
permit_list.append(TaskModel)

InsightEngine.add_pages({'task':TaskTablePage,'task.edit':TaskFormPage})
InsightEngine.add_pages({'workloads':WorkTablePage,'workloads.edit':WorkFormPage})
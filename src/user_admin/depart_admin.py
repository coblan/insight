#encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelTable,TrivalPageNum,TablePage,model_page_dc,ModelFields,model_dc
from .models import Department

class DepartmentFields(ModelFields):
    class Meta:
        model=Department
        exclude=[]
    
    def get_heads(self):
        heads=super(DepartmentFields,self).get_heads()
        for head in heads:
            if head.get('name')=='detail':
                head['type']='richtext'
        return heads

class DepartmentTable(ModelTable):
    model=Department
    exclude=[]
    pagenator=TrivalPageNum

class DepartmentTablePage(TablePage):
    template='user_admin/company.html'
    tableCls=DepartmentTable
    
    def get_context(self):
        ctx = super(DepartmentTablePage,self).get_context()
        ctx['depart_heads']=DepartmentFields(crt_user=self.crt_user).get_heads()
        return ctx


model_dc[Department]={'fields':DepartmentFields}
model_page_dc['department']={'table':DepartmentTablePage}
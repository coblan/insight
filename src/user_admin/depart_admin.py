#encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelTable,TrivalPageNum,TablePage,model_page_dc,ModelFields,model_dc
from .models import Department

class DepartmentFields(ModelFields):
    class Meta:
        model=Department
        exclude=[]

class DepartmentTable(ModelTable):
    model=Department
    exclude=[]
    pagenator=TrivalPageNum

class DepartmentTablePage(TablePage):
    template='user_admin/company.html'
    tableCls=DepartmentTable


model_dc[Department]={'fields':DepartmentFields}
model_page_dc['department']={'table':DepartmentTablePage}
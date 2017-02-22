# encoding:utf-8
from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from models import BasicInfo,MM,Fore,EmployeeModel,SalaryRecords,Month
from django.apps import apps

from helpers.director.db_tools import to_dict,model_to_name,model_to_head,sim_dict
from helpers.director.model_admin.fields import ModelFields
from helpers.director.model_admin.tabel import ModelTable,RowSearch,RowFilter,RowSort,PageNum
from helpers.director.model_admin.render import model_page_dc,model_dc,render_dc
from helpers.director.model_admin.permit import permit_list,Permit
from helpers.director.model_admin.render import TablePage,FormPage
from django.contrib.auth.models import User,Group
import json
import ajax
from django.db import models
from django.db.models import Q
from django.conf import settings
import importlib
from helpers.director.container import evalue_container

# Register your models here.
# class BasicAdmin(admin.ModelAdmin):
admin.site.register(BasicInfo)
admin.site.register(MM)
admin.site.register(Fore)
admin.site.register(EmployeeModel)
admin.site.register(SalaryRecords)
admin.site.register(Month)
#admin.site.register(PermitModel)

site_option=importlib.import_module(settings.SITE_OPTION)

class BaseSearch(RowSearch):
    names=['name']
    model=BasicInfo

class BaseFilter(RowFilter):
    names=['name','age']
    model=BasicInfo

class BaseSort(RowSort):
    names=['name','age']

class Twopage(PageNum):
    perPage=20
    
class BasicInfoTable(ModelTable):
    model = BasicInfo
    search=BaseSearch
    filters = BaseFilter
    sort=BaseSort
    include=['name','age','user']
    pagenator=Twopage
    #filters=['name','age']
    #include = ['name','age']
    #sortable=['age']
    #per_page=2
    #search_fields=['age','name']
    
    #def get_rows(self):
        #query=self.get_query()
        #ls=[]
        #for info in query:
            #info.employeemodel.user
        #return [to_dict(x,filt_attr=lambda x:{'user':str(x.user) if x.user else '---'}, include=self.permited_fields()) for x in query]         
    #def get_heads(self):
        #heads = super(BasicInfoTable,self).get_heads()
        #heads.extend([{'name':'salary','label':'工资'},
                      #])
        #return heads    
    
    #def get_rows(self):
        #rows=super(BasicInfoTable,self).get_rows()   
        #for row in rows:
            #baseinfo = BasicInfo.objects.get(pk=row['pk'])
            #if hasattr(baseinfo,'employeeinfo'):
                #row['salary']=baseinfo.employeeinfo.salary_level
        #return rows        
    
    #def get_context(self):
        #dc = super(BasicInfoTable,self).get_context()
        #dc['hh']={'jj':'<div>yy</div>'}
        #return dc

class BasicInfoFields(ModelFields):
    
    class Meta:
        model=BasicInfo
        fields=['name','age','head'] 
    
    #def get_fields(self):
        #return ['name','age']
    
    def clean_name(self):
        #raise forms.ValidationError('jjyy')
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError('need name')
        return name
    
    def save_form(self):
        rt = super(BasicInfoFields,self).save_form()
        if hasattr(self.instance,'employeemodel') and self.instance.employeemodel.user:
            self.instance.employeemodel.user.first_name=self.instance.name
            self.instance.employeemodel.user.save()
        return rt
    
    def get_heads(self):
        heads = super(BasicInfoFields,self).get_heads()
        for head in heads:
            if head.get('name')=='head':
                head['type']='picture'
        return heads
    
    #def get_options(self):
        #options = super(BasicInfoFields,self).get_options()
        
        #qs = User.objects.filter( Q(basicinfo__isnull=True)|Q(basicinfo = self.instance) )
        
        #options['user']=[{'value':user.pk,'label':user.username} for user in qs]
        #return options
    
        #for name,field in self.fields.items():
            #if isinstance(field,forms.models.ModelMultipleChoiceField):
                #options[name]=[{'value':x[0],'label':x[1]} for x in field.choices]            
            #elif isinstance(field,forms.models.ModelChoiceField):
                #options[name]=[{'value':x[0],'label':x[1]} for x in list(field.choices)[1:]]
            
        #return options    
    
    #def can_access_instance(self):
        #access = super(BasicInfoFields,self).can_access_instance()
        #if not access:
            #perm = 'user_admin.read_basicinfo'
            #return self.crt_user.has_perm(perm)
        #else:
            #return access
        
    # def get_readonly_fields(self):
        # access = super(BasicInfoFields,self).can_access_instance()
        # if not access:
            # perm = 'user_admin.read_basicinfo'
            # if self.crt_user.has_perm(perm):
                # return self.fields.keys()
        # else:
            # return access
    
        
        
#class UserTable(ModelTable):
    #model=User
    #exclude=['password','id']
    
    #def get_heads(self):
        #heads = super(UserTable,self).get_heads()
        #heads.extend([{'name':'age','label':'年龄'},
                      #{'name':'_name','label':'姓名'}])
        #return heads
    
    #def get_rows(self):
        #rows=super(UserTable,self).get_rows()
        #for user_dc in rows:
            #user = User.objects.get(pk=user_dc['pk'])
            #if hasattr(user,'basicinfo'):
                #user_dc['age']=user.basicinfo.age
                #user_dc['_name']=user.basicinfo.name
        #return rows

#class UserFields(ModelFields):
    # age = forms.CharField(label='年龄')
    
    #def pop_fields(self):
        #self.fields.pop('user_permissions')
        # if not hasattr(self.instance,'basicinfo'):
            # self.fields.pop('age')

        #self.fields.pop('username')       
    
    #def init_value(self):
        #super(UserFields,self).init_value()
        # ls =['age']
        # for k in ls:
            # if k in self.fields:
                # self.fields[k].initial=self.instance.basicinfo.age
    
    #class Meta:
        #model=User
        #fields=['username','first_name','is_active','is_staff','is_superuser','email','groups']
    
    #def get_row(self):
        #row = super(UserFields,self).get_row()
        #if row['pk']:
            #user = User.objects.get(pk= row['pk'])
            #if hasattr(user,'basicinfo'):
                #if 'age' in self.fields:
                    #row['age']=user.basicinfo.age
        #return row
    
    #def can_access_instance(self):
        #return self.crt_user.has_perm('auth.change_user') or self.crt_user.has_perm('user_admin.read_basicinfo')
    
    #def get_readonly_fields(self):
        #if not self.crt_user.has_perm('auth.change_user') and\
           #self.crt_user.has_perm('user_admin.read_basicinfo'):
            #return self.fields.keys()
        #else:
            #return []
    
    #def get_input_type(self):
        #return {'age':'text'}
    
    #def get_options(self):
        #return super(UserFields,self).get_options()
    
    #def clean_age(self):
        #print('in age function')
        #return self.cleaned_data['age']
    

class EmploySearch(RowSearch):
    model=EmployeeModel
    
    def get_context(self):
        return '姓名'

    def get_query(self,query):
        if self.q:
            exp=None
            return query.filter(baseinfo__name__icontains=self.q)
            #for name in self.valid_name:
                #kw ={}
                #kw['%s__icontains'%name] =self.q    
                #if exp is None:
                    #exp = Q(**kw)
                #else:
                    #exp = exp | Q(**kw) 
            #return query.filter(exp)
        else:
            return query
    

class EmployeeTable(ModelTable):
    model=EmployeeModel
    search=EmploySearch
    include=['employ_id','position','salary_level']
    def get_heads(self):
        heads = super(EmployeeTable,self).get_heads()
        permit = Permit(model=BasicInfo,user=self.crt_user)
        bas_field=permit.readable_fields()
        bas_heads=model_to_head(model=BasicInfo,include=bas_field)
        heads.extend(bas_heads)
        # heads.insert(1,{'name':'name','label':'姓名'})
        return heads
    
    def get_rows(self):
        rows = super(EmployeeTable,self).get_rows()
        for row in rows:
            emp = EmployeeModel.objects.get(pk=row['pk'])
            
            permit = Permit(model=BasicInfo,user=self.crt_user)
            bas_field=permit.readable_fields()            
            if emp.baseinfo:
                row.update(sim_dict(emp.baseinfo,include=bas_field))
                # row['name']=emp.baseinfo.name
        return rows
        

class EmployeeFields(ModelFields):
    class Meta:
        model=EmployeeModel
        fields=['employ_id','position','salary_level','baseinfo','user']
    
    def get_options(self):
        print(site_option.get_value('jjer'))
        site_option.set_value('jjer','cvhiui')
        options = super(EmployeeFields,self).get_options()
        
        qs = BasicInfo.objects.filter( Q(employeemodel__isnull=True)|Q(employeemodel = self.instance) )
        
        options['baseinfo']=[{'value':baseinfo.pk,'label':baseinfo.name} for baseinfo in qs]
        return options    
    
    def save_form(self):
        rt = super(EmployeeFields,self).save_form()
        if self.instance.user and self.instance.baseinfo:
            self.instance.user.first_name=self.instance.baseinfo.name
            self.instance.user.save()
        return rt

#class EmployeeSet(FieldsSet):
    #template='fieldsset.html'
    #def get_context(self):
        #ctx={}
        #if self.pk:
            #employee = EmployeeInfo.objects.get(pk=self.pk)
        #else:
            #employee= EmployeeInfo()
        #em_form = EmployeeFields(instance=employee,crt_user=self.crt_user)
        #em_context=em_form.get_context()
        #em_context['label']='员工信息'
      
        #ctx['employee_info']=em_context
        
        #if hasattr(employee,'baseinfo') and employee.baseinfo:
            #bs = BasicInfoFields(instance=employee.baseinfo,crt_user=self.crt_user)
            #bs_context=bs.get_context()
            #bs_context['label']='基本信息'
            #ctx['bs_info']=bs_context
            
            #if hasattr(employee.baseinfo,'user'):
                #user_form = UserFields(instance=employee.baseinfo.user,crt_user=self.crt_user)
                #user_context=user_form.get_context()
                #user_context['label']='账号信息'

                #ctx['user_account']=user_context   
        #return ctx


#class EmployeeProd(FieldsSet):
    #template='user_admin/employee.html'
    #def get_context(self):
        #if self.pk:
            #employee = EmployeeInfo.objects.get(pk=self.pk)
        #else:
            #employee= EmployeeInfo()
        #em_form = EmployeeFields(instance=employee,crt_user=self.crt_user)
        #em_form.fields.pop('baseinfo')
        #em_context=em_form.get_context()
        #em_context['label']='员工信息'
      
        #if not hasattr(employee,'baseinfo'):
            #employee.baseinfo=BasicInfo()

        #bs = BasicInfoFields(instance=employee.baseinfo,crt_user=self.crt_user)
        #bs_context=bs.get_context()
        #bs_context['label']='基本信息'
        #return {'employee_info':em_context,'bs_info':bs_context}
    

#class SalarySearch(SearchQuery):
    #def get_query(self,query,q,crt_user):
        #try:
            #return query.filter(empoyee__id__icontains=int(q))
        #except:
            #return query.filter(empoyee__baseinfo__name__icontains=q)
    
    #def get_placeholder(self):
        #return '员工ID或者姓名'


class SalarySearch(RowSearch):
    model=SalaryRecords
    def get_context(self):
        return '员工姓名'

    def get_query(self,query):
        if self.q:
            exp=None
            return query.filter(empoyee__baseinfo__name__icontains=self.q)
            #for name in self.valid_name:
                #kw ={}
                #kw['%s__icontains'%name] =self.q    
                #if exp is None:
                    #exp = Q(**kw)
                #else:
                    #exp = exp | Q(**kw) 
            #return query.filter(exp)
        else:
            return query    

class SalaryTabel(ModelTable):
    model=SalaryRecords
    include=['empoyee','base_salary','merit_pay','allowance','social_security','reserved_funds']
    search=SalarySearch
    #search_fields=[SalarySearch()]
    
    def get_heads(self):
        heads = super(SalaryTabel,self).get_heads()
        heads[0]['label']='员工ID'
        heads.insert(1,{'name':'name','label':'员工名字'})
        return heads
    
    def get_rows(self):
        rows=super(SalaryTabel,self).get_rows()
        for salary_dc in rows:
            emp = EmployeeModel.objects.get(pk=salary_dc['empoyee'])
            salary_dc['empoyee']=emp.employ_id
            if emp.baseinfo:
                salary_dc['name']=emp.baseinfo.name
        return rows    
    

class SalaryFields(ModelFields):
    class Meta:
        model=SalaryRecords
        fields=['empoyee','base_salary','merit_pay','allowance','social_security','reserved_funds']        


    
class SalaryTablePage(TablePage):
    tableCls=SalaryTabel

class SalaryFormPage(FormPage):
    template='user_admin/salary_form.html'
    fieldsCls=SalaryFields

class BaseinfoTablePage(TablePage):
    tableCls=BasicInfoTable
    #def __init__(self,request):
        #super(BaseinfoTablePage,self).__init__(request)
    
    #def get_context(self):
        #return self.table.get_context()

class BaseinfoFormPage(FormPage):
    fieldsCls=BasicInfoFields
    # def get_context(self):
        # return BasicInfoFields(pk=self.pk,crt_user=self.request.user).get_context()


    
class EmployeeTablePage(TablePage):
    template='user_admin/employee_table.html'
    tableCls=EmployeeTable
    
    
    
    
class EmployeeFormPage(FormPage):

    template='user_admin/employee_ok.html'

    def __init__(self,request,pk):
        self.request=request
        self.pk=pk
        
        if not self.pk:
            empfld=EmployeeFields(pk=None,crt_user=request.user)
            basfld=BasicInfoFields(pk=None,crt_user=request.user) 
        else:
            employee= EmployeeModel.objects.get(pk=self.pk)
            empfld=EmployeeFields(instance=employee,crt_user=request.user)
            if not employee.baseinfo:
                employee.baseinfo=BasicInfo.objects.create()
                employee.save()
            basfld=BasicInfoFields(instance=employee.baseinfo,crt_user=self.request.user)   

        self.pages={
            'emp_info':{'heads':empfld.get_heads(),'row':empfld.get_row(),'label':'工作信息'},
            'bas_info':{'heads':basfld.get_heads(),'row':basfld.get_row(),'label':'基本信息'}            
        }
    
    def get_context(self):
        
        #emp= self.pages #evaluse_container(self.pages)
        ctx={'person':self.pages}
        pop = self.request.GET.get('_pop')
        if not pop:
            ctx['menu']=evalue_container(render_dc.get('menu'),user=self.request.user)  
        return ctx    
    
#class UserTablePage(TablePage):
    #tableCls=UserTable

#class UserFormPage(FormPage):
    #fieldsCls=UserFields



#permit_dc['basicinfo']={'label':'个人信息','model':BasicInfo}
#permit_dc['employee']={'label':'工作信息','model':EmployeeInfo}
#permit_dc['salary_records']={'label':'工资记录','model':SalaryRecords}
permit_list.append(BasicInfo)
permit_list.append(EmployeeModel)
permit_list.append(SalaryRecords)
#permit_list.append({'name':'spcial','label':'工作权限','fields':[
                        #{'name':'sp1','label':'所有工作','type':'bool'},
                        #{'name':'sp2','label':'工作统计','type':'bool'}
                    #]})


model_dc[BasicInfo]={'fields':BasicInfoFields}
model_dc[EmployeeModel]={'fields':EmployeeFields}
model_dc[SalaryRecords]={'fields':SalaryFields}
#model_dc[User]={'fields':UserFields}

#model_render_dc['basicinfo'] ={'model':BasicInfo,'table':BasicInfoTable,'fields':BasicInfoFields,'ajax':ajax.get_globe(),'label':'员工基本信息'}
#model_page_dc['user'] = {'model':User,'table':UserTable,'fields':UserFields,'label':'账号数据'}
#model_page_dc['group']={'model':Group,'table':UserGroupTable,'fields':UserGroupFields,'ajax':ajax.get_globe(),}
#model_page_dc['employee']={'model':EmployeeInfo,'table':EmployeeTable,'fields':EmployeeFields,'label':'工作信息'}
##model_render_dc['employee_set']={'table':EmployeeTable,'fields':EmployeeSet,}
##model_render_dc['employee_prod'] ={'table':EmployeeTable,'fields':EmployeeProd,'ajax':ajax.get_globe()}
#model_page_dc['salary_records']={'table':SalaryTabel,'fields':SalaryFields,'model':SalaryRecords}

#model_page_dc['user']={'table':UserTablePage,'form':UserFormPage}

model_page_dc['basicinfo']={'table':BaseinfoTablePage,'form':BaseinfoFormPage}
model_page_dc['employee']={'table':EmployeeTablePage,'form':EmployeeFormPage}
model_page_dc['salary']={'table':SalaryTablePage,'form':SalaryFormPage}

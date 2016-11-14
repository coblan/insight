# encoding:utf-8
from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from models import BasicInfo,MM,Fore,EmployeeInfo,SalaryRecords,Month
from django.apps import apps
from director.model_admin.fields import ModelFields
from director.model_admin.tabel import ModelTable 
from director.model_admin.render import model_page_dc,model_dc
from director.model_admin.permit import permit_dc
from director.model_admin.render import TablePage,FormPage
from django.contrib.auth.models import User,Group
import json
import ajax




# Register your models here.
# class BasicAdmin(admin.ModelAdmin):
admin.site.register(BasicInfo)
admin.site.register(MM)
admin.site.register(Fore)
admin.site.register(EmployeeInfo)
admin.site.register(SalaryRecords)
admin.site.register(Month)
#admin.site.register(PermitModel)


class BasicInfoTable(ModelTable):
    model = BasicInfo
    filters=['name','age']
    include = ['name','age']
    sortable=['age']
    per_page=2
    search_fields=['age','name']
    
    def get_heads(self):
        heads = super(BasicInfoTable,self).get_heads()
        heads.extend([{'name':'salary','label':'工资'},
                      ])
        return heads    
    
    def get_rows(self):
        rows=super(BasicInfoTable,self).get_rows()   
        for row in rows:
            baseinfo = BasicInfo.objects.get(pk=row['pk'])
            if hasattr(baseinfo,'employeeinfo'):
                row['salary']=baseinfo.employeeinfo.salary_level
        return rows        
    
    def get_context(self):
        dc = super(BasicInfoTable,self).get_context()
        dc['hh']={'jj':'<div>yy</div>'}
        return dc

class BasicInfoFields(ModelFields):
    
    class Meta:
        model=BasicInfo
        fields=['name','age','user'] 
    
    def get_fields(self):
        return ['name','age']
    
    def clean_name(self):
        return self.cleaned_data['name']
    
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
    
        
        
class UserTable(ModelTable):
    model=User
    include=['username','first_name']
    
    def get_heads(self):
        heads = super(UserTable,self).get_heads()
        heads.extend([{'name':'age','label':'年龄'},
                      {'name':'_name','label':'姓名'}])
        return heads
    
    def get_rows(self):
        rows=super(UserTable,self).get_rows()
        for user_dc in rows:
            user = User.objects.get(pk=user_dc['pk'])
            if hasattr(user,'basicinfo'):
                user_dc['age']=user.basicinfo.age
                user_dc['_name']=user.basicinfo.name
        return rows

class UserFields(ModelFields):
    # age = forms.CharField(label='年龄')
    
    def pop_fields(self):
        self.fields.pop('user_permissions')
        # if not hasattr(self.instance,'basicinfo'):
            # self.fields.pop('age')

        #self.fields.pop('username')       
    
    def init_value(self):
        super(UserFields,self).init_value()
        # ls =['age']
        # for k in ls:
            # if k in self.fields:
                # self.fields[k].initial=self.instance.basicinfo.age
    
    class Meta:
        model=User
        fields=['username','first_name','is_active','is_staff','is_superuser','email','groups','user_permissions']
    
    def get_row(self):
        row = super(UserFields,self).get_row()
        if row['pk']:
            user = User.objects.get(pk= row['pk'])
            if hasattr(user,'basicinfo'):
                if 'age' in self.fields:
                    row['age']=user.basicinfo.age
        return row
    
    def can_access_instance(self):
        return self.crt_user.has_perm('auth.change_user') or self.crt_user.has_perm('user_admin.read_basicinfo')
    
    def get_readonly_fields(self):
        if not self.crt_user.has_perm('auth.change_user') and\
           self.crt_user.has_perm('user_admin.read_basicinfo'):
            return self.fields.keys()
        else:
            return []
    
    def get_input_type(self):
        return {'age':'text'}
    
    def get_options(self):
        return super(UserFields,self).get_options()
    
    def clean_age(self):
        print('in age function')
        return self.cleaned_data['age']
    

class UserGroupTable(ModelTable):
    model=Group
    include=['name','permissions']


class UserGroupFields(ModelFields):
    template='user_admin/permit.html'
    class Meta:
        model=Group
        fields=['name',]
        
    # def get_heads(self):
        # heads = super(UserGroupFields,self).get_heads()
        # for head in heads:
            # if head['name']==:
                # head['size']=20
        # return heads
    def get_context(self):
        ctx = super(UserGroupFields,self).get_context()
        group = self.instance
        #if not hasattr(group,'permitmodel'):
            #group.permitmodel=PermitModel.objects.create(group=group)
        if hasattr(group,'permitmodel'):
            ctx['permits']=json.loads(group.permitmodel.permit) #[{'model':x.model,'permit': json.loads(x.permit)} for x in self.instance.per.all()]
        ls = []
        # for k1,v1 in apps.all_models.items():
            # for k2,v2 in v1.items():
                # ls.append({'name':'%s.%s'%(k1,k2),'label':'%s.%s'%(k1,k2)})
        for k,v in model_dc.items():
            if v.has_key('model'):
                ls.append({'name':k,'label':v.get('label',k)})
        ctx['models']=ls
        
        return ctx


class EmployeeTable(ModelTable):
    model=EmployeeInfo
    include=['employ_id','position','salary_level']
    def get_heads(self):
        heads = super(EmployeeTable,self).get_heads()
        heads.insert(1,{'name':'name','label':'姓名'})
        return heads
    
    def get_rows(self):
        rows = super(EmployeeTable,self).get_rows()
        for row in rows:
            emp = EmployeeInfo.objects.get(pk=row['pk'])
            row['name']=emp.baseinfo.name
        return rows
        

class EmployeeFields(ModelFields):
    class Meta:
        model=EmployeeInfo
        fields=['employ_id','position','salary_level','baseinfo']

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
    
class SalaryTabel(ModelTable):
    model=SalaryRecords
    include=['empoyee','base_salary','merit_pay','allowance','social_security','reserved_funds']
    #search_fields=[SalarySearch()]
    
    def get_heads(self):
        heads = super(SalaryTabel,self).get_heads()
        heads[0]['label']='员工ID'
        heads.insert(1,{'name':'name','label':'员工名字'})
        return heads
    
    def get_rows(self):
        rows=super(SalaryTabel,self).get_rows()
        for salary_dc in rows:
            emp = EmployeeInfo.objects.get(pk=salary_dc['empoyee'])
            salary_dc['empoyee']=emp.employ_id
            if emp.baseinfo:
                salary_dc['name']=emp.baseinfo.name
        return rows    
    

class SalaryFields(ModelFields):
    class Meta:
        model=SalaryRecords
        fields=['empoyee','base_salary','merit_pay','allowance','social_security','reserved_funds']        



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
    

permit_dc['basicinfo']={'label':'个人信息','model':BasicInfo}
permit_dc['employee']={'label':'工作信息','model':EmployeeInfo}
permit_dc['salary_records']={'label':'工资记录','model':SalaryRecords}

model_dc[BasicInfo]={'fields':BasicInfoFields}
#model_render_dc['basicinfo'] ={'model':BasicInfo,'table':BasicInfoTable,'fields':BasicInfoFields,'ajax':ajax.get_globe(),'label':'员工基本信息'}
model_page_dc['user'] = {'model':User,'table':UserTable,'fields':UserFields,'label':'账号数据'}
model_page_dc['group']={'model':Group,'table':UserGroupTable,'fields':UserGroupFields,'ajax':ajax.get_globe(),}
model_page_dc['employee']={'model':EmployeeInfo,'table':EmployeeTable,'fields':EmployeeFields,'label':'工作信息'}
#model_render_dc['employee_set']={'table':EmployeeTable,'fields':EmployeeSet,}
#model_render_dc['employee_prod'] ={'table':EmployeeTable,'fields':EmployeeProd,'ajax':ajax.get_globe()}
model_page_dc['salary_records']={'table':SalaryTabel,'fields':SalaryFields,'model':SalaryRecords}

model_page_dc['basicinfo']={'table':BaseinfoTablePage,'form':BaseinfoFormPage}

#from core.model_render import save_row,model_dc
from helpers.director.db_tools import name_to_model,sim_dict,from_dict
from helpers.director.models import PermitModel
from helpers.director.model_admin.render import model_dc
from helpers import ex

from django.contrib.auth.models import Group
import json
from models import EmployeeModel,SalaryRecords,Department
from django.core.exceptions import ValidationError
from helpers.director.shortcut import save_row,ModelPermit
from helpers.shortcuts import _



def get_globe():
    return globals()

#def save_employ_infos(employee_info=None,bs_info=None,user=None):
    #dc={}
    #if bs_info:
        #bs_form = save_row(bs_info,user)
        #dc['bs_errors']=bs_form.errors
    #if not bs_form.errors :
        #employee_info['baseinfo'] =bs_form.instance.pk
        
    #if employee_info:
        #emp_form = save_row(employee_info, user)
        #dc['employee_errors']=emp_form.errors
    
    #return dc   
    

def save_employee_info(user,emp_info,bas_info):
    try:
        emp = save_row(emp_info, user)
    except ValidationError as e:
        return {'emp_errors':dict(e)}  
    try:
        bas_info= save_row(bas_info,user)
    except ValidationError as e:
        return {'bas_errors':dict(e)} 
    
    if not emp.baseinfo:
        emp.baseinfo=bas_info
        emp.save()
    return {'status':'success'}



def model_permit_info(name,user):
    model = name_to_model(name)
    fields = model_dc.get(model).get('fields')
    ls=[]
    for k,v in fields(crt_user=user).fields.items():
        if hasattr(v.label,'title') and callable(v.label.title):
            label=v.label.title()
        else:
            label=v.label
            
        ls.append({'name':k,'label':label})
    return ls


def save_group_and_permit(row,permits,user): 
    field_cls = model_dc.get(Group).get('fields')
    group_form= field_cls(row, crt_user= user)
    if group_form.is_valid():
        group_form.save_form()
    group = group_form.instance
    if not hasattr(group,'permitmodel'):
        PermitModel.objects.create(group=group)
    group.permitmodel.permit=json.dumps(permits)
    group.permitmodel.save()
    
    # perm={'group':group_form.instance.pk,'permit':permits}
    # perm_form = save_row(perm, user)
    return {'status':'success'}


def employee_info(pk):
    employee = EmployeeModel.objects.get(pk=pk)
    return {'status':'success',
            'employee':sim_dict(employee)
            }

def creat_month_salary_all(month,user):
    permit = ModelPermit(SalaryRecords,user)
    if permit.can_add():
        for emp in EmployeeModel.objects.all():
            SalaryRecords.objects.get_or_create(empoyee=emp,base_salary=emp.salary_level,month=month)
        
    return {'status':'success','msg':_('operation sucess')}

def make_sure(salary_pks,user):
    permit = ModelPermit(SalaryRecords,user)
    if 'is_checked' in permit.changeable_fields():
        SalaryRecords.objects.filter(pk__in=salary_pks).update(is_checked=True)
    
    return {'status':'success','msg':_('operation sucess')}


def save_departments(rows,user,deleted_departs=[]):
    #Permit(model, user)
    for depart in rows:
        if not depart.get('pk',None):
            obj = Department.objects.create(label=depart.get('label'))
            depart['pk']=obj.pk
    
    for depart in rows:
        par =depart.get('par')
        if par :
            par_depart = ex.findone(rows,{'did':par}) 
            if par_depart:
                depart['par']=par_depart.get('pk')
    
    for depart in rows:
        #depart.pop('did')
        depart_obj = from_dict(depart,model=Department)
        depart_obj.save()
        #Department.objects.update(**depart)
    
    for depart in deleted_departs:
        if depart.get('pk'):
            Department.objects.filter(pk=depart.get('pk')).delete()
    
    return {'status':'success'}
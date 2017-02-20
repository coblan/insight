#from core.model_render import save_row,model_dc
from helpers.director.db_tools import name_to_model,sim_dict
from helpers.director.models import PermitModel
from helpers.director.model_admin.render import model_dc
from django.contrib.auth.models import Group
import json
from models import EmployeeModel
from django.core.exceptions import ValidationError
from helpers.director.shortcut import save_row


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
    

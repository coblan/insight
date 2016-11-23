# encoding:Utf-8
from __future__ import unicode_literals
from django.apps import apps
from permit import Permit
from base import model_dc,get_admin_name_by_model,del_row


def get_globle():
    return globals()


def model_perm(user,perm,model):
    validator = Permit(model, user)
    return getattr(validator,perm)()

def save(row,user):
    """
    """
    # edit = re.search('^(\w+)/edit/(\w*)/?$',self.url)
    model= apps.get_model(row['_class'])
    admin_name = get_admin_name_by_model(model)
    model_item = model_dc.get(admin_name) 
    fields_cls = model_item.get('fields') 
    row['crt_user']=user
    fields_obj=fields_cls(row,crt_user=user)
    if fields_obj.is_valid():
        return fields_obj.save_form()
    else:
        return {'errors':fields_obj.errors}


def del_rows(rows,user):
    for row in rows:
        del_row(row, user)
        
    return {'status':'success','rows':rows}  
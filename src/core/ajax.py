# encoding:Utf8
from __future__ import unicode_literals
from django.apps import apps

# used for model render
model_dc={
    #'xxx_model': {'model':'xxx','table_temp':xxx,'field_temp':xxx}
}

def get_globle():
    return globals()


def has_perm(user,perm):
    return user.has_perm(perm)


def get_admin_name_by_model(model):
    if model:
        for k,v in model_dc.items():
            if v.get('model')==model:
                return k

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
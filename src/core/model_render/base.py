from django.apps import apps

# used for model render
model_dc={
    #'xxx_model': {'model':'xxx','table_temp':xxx,'field_temp':xxx}
}


def get_admin_name_by_model(model):
    if model:
        for k,v in model_dc.items():
            if v.get('model')==model:
                return k


def del_row(row,user):
    model= apps.get_model(row['_class'])
    admin_name = get_admin_name_by_model(model)    
    model_item = model_dc.get(admin_name) 
    fields_cls = model_item.get('fields')
    fields_obj=fields_cls(row,crt_user=user)
    return fields_obj.del_instance() 

def save_row(row,user):
    """
    used by inner system ,save row handly
    """
    model= apps.get_model(row['_class'])
    admin_name = get_admin_name_by_model(model)    
    model_item = model_dc.get(admin_name) 
    fields_cls = model_item.get('fields')
    fields_obj=fields_cls(row,crt_user=user)
    if fields_obj.is_valid():
        fields_obj.save_form()
    return fields_obj
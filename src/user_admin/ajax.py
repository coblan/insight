from core.model_render import save_row,model_dc

def get_globe():
    return globals()

def save_employ_infos(employee_info=None,bs_info=None,user=None):
    dc={}
    if bs_info:
        bs_form = save_row(bs_info,user)
        dc['bs_errors']=bs_form.errors
    if not bs_form.errors :
        employee_info['baseinfo'] =bs_form.instance.pk
        
    if employee_info:
        emp_form = save_row(employee_info, user)
        dc['employee_errors']=emp_form.errors
    
    return dc    

def admin_fields(name,user):
    fields = model_dc.get(name).get('fields')
    ls=[]
    for k,v in fields(crt_user=user).fields.items():
        if hasattr(v.label,'title') and callable(v.label.title):
            label=v.label.title()
        else:
            label=v.label
            
        ls.append({'name':k,'label':label})
    return ls


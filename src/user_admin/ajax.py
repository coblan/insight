from core.model_render import save_row

def get_globe():
    return globals()

def save_employ_infos(employee_info,bs_info,user_account,user):
    dc={}
    if employee_info:
        emp_dc = save_row(employee_info, user)
        dc['employee_errors']=emp_dc.errors
    if bs_info:
        bs_dc = save_row(bs_info,user)
        dc['bs_errors']=bs_dc.errors
    if user_account:
        user_dc = save_row(user_account,user)
        dc['user_errors']=user_dc.errors

    return dc    

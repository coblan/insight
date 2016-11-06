
def evalue_container(container,*args,**kw):
    """
    use to evalue dict or list ,that has some callable element
    
    Example:
    dc={'name':lambda user:user.username}
    
    dc = evalue_container(dc,user=request.user)
    
    """
    if isinstance(container,dict):
        return evalue_dict(container,*args,**kw)
    elif isinstance(container,(tuple,list)):
        return evalue_list(container,*args,**kw)
    elif callable(container):
        return container(*args,**kw)
    else:
        return container

def evalue_dict(dc,*args,**kw):
    for k,v in dc.items():
        dc[k]=evalue_container(v,*args,**kw)
    return dc

def evalue_list(ls,*args,**kw):
    new_ls=[]
    for item in ls:
        tmp=evalue_container(item,*args,**kw)
        if isinstance(tmp,dict) and tmp.get('invalid'):
            continue
        new_ls.append(tmp)
    return new_ls
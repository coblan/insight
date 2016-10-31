
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
        # temp_act ={}
        # for k,v in act.items():
            # if callable(v):
                # temp_act[k]=v(self.request.user)
            # elif isinstance(v,(list,tuple)):
                # temp_act[k]=self._evalue_menu_dict(v)
            # else:
                # temp_act[k]=v
        # if not 'valid' in temp_act or temp_act['valid']: # only valid ,this menu will be display
            # temp_menu.append(temp_act)
    return dc

def evalue_list(ls,*args,**kw):
    index=0
    for item in ls:
        ls[index]=evalue_container(item,*args,**kw)
        index+=1
    return ls
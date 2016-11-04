from __future__ import unicode_literals
from model_render import model_dc
from ajax import get_admin_name_by_model
import json

class Permit(object):
    def __init__(self,inst,user):
        self.user=user
        self.model = inst._meta.model
        self.permit_list=[]
        self._init_perm()
    
    def _init_perm(self):
        admin_name = get_admin_name_by_model(self.model)
        for group in self.user.groups.all():
            if hasattr(group,'permitmodel'):
                permits = json.loads( group.permitmodel.permit )
                for permit in permits:
                    if permit.get('admin_name') == admin_name:
                        self.permit_list.append(permit.get('row'))
                
    def can_add(self):
        for row in self.permit_list:
            if 'can_add' in row:
                return True
    
    def can_del(self):
        for row in self.permit_list:
            if 'can__create' in row:
                return True        
    
    def readonly_fields(self):
        return [x for x in self.readable_fields() if x not in self.changeable_fields()]
    
    def readable_fields(self):
        ls =[]
        for row in self.permit_list:
            for key in row:
                if key.endswith('__read'):
                    ls.append(key[0:-6])
        return list(set(ls))  
    
    def changeable_fields(self):
        ls = []
        for row in self.permit_list:
            for key in row:
                if key.endswith('__write'):
                    ls.append(key[0:-7])
        return list(set(ls))
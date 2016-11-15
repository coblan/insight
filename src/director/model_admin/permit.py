# encoding:utf8

from __future__ import unicode_literals
from director.db_tools import model_to_name
from django.apps import apps
import json

permit_dc={}

class Permit(object):
    """
    以json的形式存储于permitModel数据库
    
    [{'model':'app.App',}]
    """
    def __init__(self,model,user):
        self.user=user
        if isinstance(model,(str,unicode)):
            model=apps.get_model(model)
        self.model = model
        self.permit_list=[]
        self._init_perm()
    
    def _init_perm(self):
        model_name = model_to_name(self.model)
        for group in self.user.groups.all():
            if hasattr(group,'permitmodel'):
                permits = json.loads( group.permitmodel.permit )
                for permit in permits:
                    if permit.get('model') == model_name:
                        self.permit_list.extend(permit.get('row'))
        self.permit_list=list(set(self.permit_list))
                
    def can_add(self):
        if self.user.is_superuser:
            return True
        else:
            return 'can__create' in self.permit_list

    def can_del(self):
        if self.user.is_superuser:
            return True
        else:
            return 'can__delete' in self.permit_list
    
    def can_access(self):
        if self.user.is_superuser:
            return True
        elif self.readable_fields() or self.changeable_fields():
            return True
        else:
            return False

    def readonly_fields(self):
        if self.user.is_superuser:
            return []
        else:
            return [x for x in self.readable_fields() if x not in self.changeable_fields()]
    
    def all_fields(self):
        ls=[]
        for field in self.model._meta.fields:
            ls.append(field.name)   
        return ls
    
    def readable_fields(self):
        if self.user.is_superuser:
            return self.all_fields()
        else:
            ls=[]
            for perm in self.permit_list:
                if perm.endswith('__read'):
                    ls.append(perm[0:-6])
            return list(set(ls))  
    
    def changeable_fields(self):
        if self.user.is_superuser:
            return self.all_fields()
            #return self.model._meta.get_all_field_names()
        else:
            ls = []
            for perm in self.permit_list:
                if perm.endswith('__write'):
                    ls.append(perm[0:-7])
            return list(set(ls))
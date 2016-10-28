# encoding:utf-8
from __future__ import unicode_literals
from django import forms
from db_tools import form_to_head,to_dict,get_or_none,delete_related_query
from django.http import Http404
import json
from django.db import models
from django.core.exceptions import PermissionDenied
from db_tools import from_dict


class ModelFields(forms.ModelForm):
    """
    Only @model is must
    """

    def __init__(self,dc={},pk=None,crt_user=None,*args,**kw):
        
        # pk = dc.get('pk',None)
        # crt_user = dc.get('crt_user',None)
        if not crt_user:
            self.crt_user=dc.get('crt_user')
        else:
            self.crt_user = crt_user
        
        if pk is None:
            pk=dc.get('pk')
        if 'instance' not in kw:
            if pk:
                kw['instance']= get_or_none( self._meta.model,pk=pk)
                if not kw['instance']:
                    raise Http404('Id that you request is not exist in database')
                
            else:
                kw['instance'] = self._meta.model()
        # self.instance = kw['instance']
        # if 'initial' not in kw:
            # kw['initial']=self.get_init_value()
        super(ModelFields,self).__init__(dc,*args,**kw)
        self.init_fields()
        self.init_value()

        # if self.get_fields():
            # self._meta.fields=self.get_fields() 

    def get_context(self):
        return {
            'heads':self.get_heads(),
            'row': self.get_row(),
        }  
    def get_del_info(self):
        return {unicode(self.instance):delete_related_query(self.instance)}
    
    def init_fields(self):
        """
        pop some field out,this will be 
        """
        pass
    
    def init_value(self):
        if self.instance.pk:
            for f in self.instance._meta.get_all_field_names():
                if f in self.fields:
                    value = getattr(self.instance,f)
                    if hasattr(value,'all'):
                        value=value.all()
                    self.fields[f].initial= value
    
    def get_heads(self):
        heads = form_to_head(self)
        for k,v in self.get_options().items():
            for head in heads:
                if head['name']==k:
                    head['options']=v
        for k,v in self.get_input_type().items():
            for head in heads:
                if head['name']==k:
                    head['type']=v
        for name in self.get_readonly_fields():
            for head in heads:
                if head['name']==name:
                    head['readonly']=True               
        return heads
    
    def can_access_instance(self):
        """
        used to judge is self.crt_user has right to access self.instance
        """
        perm = self.instance._meta.app_label+'.change_'+self.instance._meta.model_name
        return self.crt_user.has_perm(perm)
    
    def get_readonly_fields(self):
        return []
    
    def get_row(self):
        """
        convert self.instance to dict.
        Note:Only convert Meta.fields ,not All fields
        """
        if not self.can_access_instance():
            raise PermissionDenied,'you have no Permission access %s'%self.instance._meta.model_name
        
        include = [x for x in self._meta.fields if x in self.fields]
        return to_dict(self.instance,include=include)

    def get_options(self):
        options={}
        
        for name,field in self.fields.items():
            if isinstance(field,forms.models.ModelMultipleChoiceField):
                options[name]=[{'value':x[0],'label':x[1]} for x in field.choices]            
            elif isinstance(field,forms.models.ModelChoiceField):
                options[name]=[{'value':x[0],'label':x[1]} for x in list(field.choices)[1:]]
            
        return options
    
    def get_input_type(self):
        types={}
        return types
    
    def save_form(self):
        """
        call by model render engin
        """
        if self.instance.pk:
            op='change'
        else:
            op='add'
        table_perm = self.instance._meta.app_label+'.%s_'%op+self.instance._meta.model_name
        if not self.crt_user.has_perm(table_perm):
            raise PermissionDenied,'you have no Permission access %s'%self.instance._meta.model_name 
        if not self.can_access_instance():
            raise PermissionDenied,'you have no Permission access %s'%self.instance._meta.model_name  
        
        for data in self.changed_data:
            if data in self.get_readonly_fields():
                raise PermissionDenied,"Can't change {data}".format(data=data)
        
        if self.instance.pk is None:
            self.instance.save() # if instance is a new row , need save first then manytomany_relationship can create        
        for k,v in self.cleaned_data.items():
            setattr(self.instance,k,v)
        self.instance.save()
        return {'status':'success'}
    
    def del_instance(self):
        del_perm = self.instance._meta.app_label+'.del_'+self.instance._meta.model_name
        if self.crt_user.has_perm(del_perm):
            self.instance.delete()

    
    

class FieldsSet(object):
    template=''
    def __init__(self,pk=None,crt_user=None):
        self.pk=pk
        self.crt_user=crt_user
    
    def get_context(self):
        return {}
        


        
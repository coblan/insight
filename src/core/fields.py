from django import forms
from db_tools import form_to_head,to_dict,get_or_none,delete_related_query
from django.http import Http404
import json
from django.db import models

class ModelFields(forms.ModelForm):
    """
    Only @model is must
    """
    # form = 'XXX'
    #model = ''
    #fields=[]
    #exclude=[]

    def __init__(self,dc,*args,**kw):
        
        pk = dc.get('pk',None)
        crt_user = dc.get('crt_user',None)
        if 'instance' not in kw:
            if pk:
                kw['instance']= get_or_none( self._meta.model,pk=pk)
                if not kw['instance']:
                    raise Http404('Id that you request is not exist in database')
                
            else:
                kw['instance'] = self._meta.model()
        if 'initial' not in kw:
            kw['initial']=to_dict(kw['instance'])
        super(ModelFields,self).__init__(dc,*args,**kw)
        self.crt_user = crt_user
        #form_obj = cls(instance=instance,*args,**kw)

        #form_obj.user=user
        
        if self.get_fields():
            self._meta.fields=self.get_fields() 

    
    def get_context(self):
        return {
            'heads':json.dumps(self.get_heads()),
            'row': json.dumps(self.get_row()),
        }  
    
    
    
    def get_heads(self):
        heads = form_to_head(self,include=self._meta.fields)
        for k,v in self.get_options().items():
            for head in heads:
                if head['name']==k:
                    head['options']=v
        for k,v in self.get_input_type().items():
            for head in heads:
                if head['name']==k:
                    head['type']=v
        return heads
    
    def get_row(self):
        return to_dict(self.instance,include=self._meta.fields)

    
    def get_options(self):
        options={}
        
        for name,field in self._get_fields():
            if isinstance(field,models.OneToOneField):
                options[name]=[{'pk':x.pk,'label':str(x)} for x in field.related_model.objects.all()]
        
        return options
    
    
    def get_fields(self):
        return None
    
    def _get_fields(self):
        for name in self._meta.fields:
            yield name,self._meta.model._meta.get_field(name)
        
    def get_input_type(self):
        types={}
        for name,field in self._get_fields():
            if isinstance(field,models.OneToOneField):
                types[name]='sim_select'  
            
        return types
    
    #def get_read_fields(self):
        #return self.fields
    
    #def get_write_fields(self):
        #return self.fields
    
    
    

    
    

        
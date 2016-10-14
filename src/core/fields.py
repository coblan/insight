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
        self.crt_user = crt_user
        
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
            'heads':json.dumps(self.get_heads()),
            'row': json.dumps(self.get_row()),
        }  
    
    def init_fields(self):
        pass
    
    def init_value(self):
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
    
    def get_readonly_fields(self):
        return []
    
    def get_row(self):
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
    
    
    # def is_valid(self):
        # for k in self.fields:
            # if k in self.get_readonly_fields():
                # self.fields.pop(k)
        # return super(ModelFields,self).is_valid()
        
    def get_input_type(self):
        types={}
        #for name,field in self.fields.items():
            #if isinstance(field,forms.models.ModelChoiceField):
                #types[name]='sim_select'  
        return types
    
    def save(self,instane,row):
        """
        call by model render engin
        """
        for data in self.changed_data:
            if data in self.get_readonly_fields():
                raise ValueError,"Can't change {data}".format(data=data)
        instane.save()
        return {'status':'success'}
    
    

    
    

        
from django import forms
from db_tools import form_to_head,to_dict,get_or_none
from django.http import Http404
import json

class ModelFields(object):
    """
    Only @model is must
    """
    # form = 'XXX'
    model = ''
    fields=[]
    exclude=[]
    def __init__(self,pk=''):
        if not getattr(self,'form',None):
            class TempForm(forms.ModelForm):
                class Meta:
                    model=self.model
                    fields=self.fields
                    exclude=self.exclude
            self.form = TempForm
        self.pk=pk
            
    def get_context(self):
        return {
            'heads':json.dumps(self.get_heads()),
            'row': json.dumps(self.get_row()),
        }  
    
    def get_heads(self):
        return form_to_head( self.form())
    
    def get_row(self):
        if self.pk:
            inst = get_or_none( self.model,pk=self.pk)
            if inst:
                return to_dict(inst)
            else:
                raise Http404('Id that you request is not exist in database')
        else:
            return to_dict(self.model())
    

        
# encoding:utf-8
from django.shortcuts import render,Http404
from tabel import ModelTable
from fields import ModelFields
from django.forms import ModelForm
from db_tools import model_form_save
from port import jsonpost
import json
from django.apps import apps
import re

# used for model render
model_dc={
    #'xxx_model': {'model':'xxx','table_temp':xxx,'field_temp':xxx}
}

def get_url(name):
    pass

class Render(object):
    def __init__(self,request,url,table_temp,fields_temp,menu):
        """
        url:
        -----
        name/
        name/edit/1
        
        @name: rigist name of model.
        """
        self.request=request
        self.url=url
        self.table_temp=table_temp
        self.fields_temp=fields_temp
        self.menu=menu
        
        self.model_item={}
         
    def rout(self):
        if self.request.method=='POST':
            dc ={}
            for k,v in Render.__dict__.items():
                if callable(v):
                    dc[k]= getattr(self,k)
            return jsonpost(self.request, dc)   
        else:
            temp = None
            context = None
            browse = re.search('^(\w+)/?$', self.url)
            if browse:
                self.name=browse.group(1)
                self.model_item =model_dc.get(self.name)
                temp,context = self.browse()
                
            edit = re.search('^(\w+)/edit/(\w*)/?$',self.url)
            if edit:
                self.name=edit.group(1)
                self.model_item =model_dc.get(self.name)  
                self.pk=edit.group(2)
                temp, context = self.edit(name=edit.group(1),pk=edit.group(2))
            if temp is None or context is None:
                raise Http404()
            else:
                context['menu']= json.dumps(self.get_menu())
                context.update(self.extra_context())
                return render(self.request,temp,context=context) 
        
    def browse(self):
        table_cls = self.model_item.get('table',self._get_new_table_cls())
        table = table_cls.parse_request(self.request)
        if hasattr(table,'template'):
            self.table_temp = table.template

        return self.table_temp, table.get_context(self.request.user)
        
        #return render(self.request,self.table_temp,table.get_context())        
 
    def edit(self,name,pk):
        if self.request.method=='GET':
            fields_cls = self.model_item.get('fields',self._get_new_fields_cls())
            dc={'pk':self.pk,'crt_user':self.request.user}
            fields = fields_cls(dc)
            if hasattr(fields,'template'):
                self.fields_temp=fields.template
           
            return self.fields_temp,fields.get_context()       

    
    def get_menu(self):
        pop = self.request.GET.get('_pop')
        if not pop:
            return self.menu
        else:
            return {}
    
    def extra_context(self):
        return {}
    
    def _get_new_fields_cls(self):
        class TempFields(ModelFields):
            model=self.model_item.get('model')

        return TempFields   
    
    def _get_new_table_cls(self):
        class TempTable(ModelTable):
            model = self.model_item.get('model')
        return TempTable    
    
    def save(self,row,user):
        edit = re.search('^(\w+)/edit/(\w*)/?$',self.url)
        self.model_item = model_dc.get(edit.group(1)) 
        fields_cls = self.model_item.get('fields',self._get_new_fields_cls())
        row['crt_user']=user
        
        return model_form_save(fields_cls,row)



# def rout(request,url,table_temp,fields_temp):
    # """
    # name/
    # name/edit/1
    # """
    # browse = re.search('^(\w+)/?$',url)
    # if browse:
        # return render_table(request,name=browse.group(1),temp=table_temp)
    # edit = re.search('^(\w+)/edit/(\w*)/?$',url)
    # if edit:
        # return render_field(request,name=edit.group(1),pk=edit.group(2),temp=fields_temp)
    # raise Http404()
        



# def render_table(request,name,temp):
    # dc = model_dc.get(name)
    # if not dc:
        # raise Http404()
    # table_cls = dc.get('table',_get_table_cls(dc.get('model')))
    # table = table_cls.parse_request(request)
    # if hasattr(table,'template'):
        # temp=table.template
    # return render(request,temp,table.get_context())

# def _get_table_cls(model_):
    # class TempTable(ModelTable):
        # model = model_
    # return TempTable

# def render_field(request,name,pk,temp):
    # dc = model_dc.get(name)
    # if not dc:
        # raise Http404()
    # fields_cls = dc.get('fields',_get_new_fields_cls(dc.get('model')))
    # fields = fields_cls(pk=pk)
    # if hasattr(fields,'template'):
        # temp=fields.template
    # return render(request,temp,fields.get_context())

# def _get_new_fields_cls(model_):
    # # class TempForm(ModelForm):
        # # class Meta:
            # # model=model_
            # # exclude=[]
    # class TempFields(ModelFields):
        # pass
        # # form=TempForm
    
    # return TempFields
        
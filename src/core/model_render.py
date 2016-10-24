# encoding:utf-8
from django.shortcuts import render,Http404
from tabel import ModelTable
from fields import ModelFields
from django.forms import ModelForm
from db_tools import model_form_save,from_dict,delete_related_query
from port import jsonpost
import json
from django.apps import apps
import re
import base64

# used for model render
model_dc={
    #'xxx_model': {'model':'xxx','table_temp':xxx,'field_temp':xxx}
}

def get_url(name):
    pass

def get_admin_name_by_model(model):
    if model:
        for k,v in model_dc.items():
            if v.get('model')==model:
                return k

def get_fields_by_name(name):
    for k,v in model_dc.items():
        if v.get('fields') and v.get('fields').__class__.__name__==name:
            return v.get('fields')
        

class Render(object):
    def __init__(self,request,url,table_temp,fields_temp,del_rows_temp,menu):
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
        self.del_rows_temp=del_rows_temp
        self.menu=menu
        self.crt_user = self.request.user
        
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
            del_rows = re.search('^del_rows/?$',self.url)
            if del_rows:
                temp,context = self.del_rows()
            elif re.search('^(\w+)/?$', self.url):
                browse = re.search('^(\w+)/?$', self.url)
                self.name=browse.group(1)
                self.model_item =model_dc.get(self.name)
                temp,context = self.browse()
            elif re.search('^(\w+)/edit/?$',self.url):
                edit = re.search('^(\w+)/edit/?$',self.url)
                self.name=edit.group(1)
                self.model_item =model_dc.get(self.name)  
                temp, context = self.edit(name=edit.group(1),pk=None)            
            elif re.search('^(\w+)/edit/(\w*)/?$',self.url):
                edit = re.search('^(\w+)/edit/(\w*)/?$',self.url)
                self.name=edit.group(1)
                self.model_item =model_dc.get(self.name)  
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
            dc={'pk':pk,'crt_user':self.request.user}
            fields = fields_cls(**dc)
            if hasattr(fields,'template') and fields.template:
                self.fields_temp=fields.template
           
            return self.fields_temp,fields.get_context()       

    def del_rows(self):
        """
        inst_ls = base64([{pk:1,_class:app.model}])
        """
        ls_str = self.request.GET.get('inst_ls')
        ls = json.loads(base64.b64decode(ls_str))
        
        ctx = {}
        for row in ls:
            model = apps.get_model(row['_class'])
            admin_name = get_admin_name_by_model(model)
            model_item = model_dc.get(admin_name)
            fields_cls = model_item.get('fields',self._get_new_fields_cls())
            
            dc={'pk':row['pk'],'crt_user':self.request.user}
            fields_obj= fields_cls(**dc)
            ctx.update(fields_obj.get_del_info())
            
        return self.del_rows_temp,{'infos':ctx}
    
    def get_menu(self):
        pop = self.request.GET.get('_pop')
        if not pop:
            return self._evalue_menu_dict(self.menu)
        else:
            return {}
    
    def _evalue_menu_dict(self,menu):
        temp_menu=[]
        for act in menu:
            temp_act ={}
            for k,v in act.items():
                if callable(v):
                    temp_act[k]=v(self.request.user)
                elif isinstance(v,(list,tuple)):
                    temp_act[k]=self._evalue_menu_dict(v)
                else:
                    temp_act[k]=v
            if not 'valid' in temp_act or temp_act['valid']: # only valid ,this menu will be display
                temp_menu.append(temp_act)
        return temp_menu
                    
    
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
        # edit = re.search('^(\w+)/edit/(\w*)/?$',self.url)
        model= apps.get_model(row['_class'])
        admin_name = get_admin_name_by_model(model)
        if not admin_name:
            edit = re.search('^(\w+)/edit/(\w*)/?$',self.url)
            admin_name= edit.group(1)
            
        self.model_item = model_dc.get(admin_name) 
        fields_cls = self.model_item.get('fields',self._get_new_fields_cls())
        row['crt_user']=user
        return model_form_save(fields_cls,row)
    
    def get_del_info(self,rows):
        out = {}
        for row in rows:
            inst=from_dict(row)
            out[str(inst)]=delete_related_query(inst)
        return out
    
    def delete(self,):
        pass
    
    def fields_info(self,pk=None,model=None,name=None):
        """
        从前端直接读取fields的 heads rows 属性
        model and name 选择一个参数即可
        """
        if model:
            admin_name = get_admin_name_by_model(model)
            fields= model_dc.get(admin_name).get('fields')
        elif name:
            fields = get_fields_by_name(name)
        return fields(pk=pk,crt_user=self.crt_user).get_context()
            



    

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
        
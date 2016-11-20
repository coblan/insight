# encoding:utf8
from __future__ import unicode_literals

from model_admin.render import TablePage,FormPage
from model_admin.tabel import ModelTable
from model_admin.fields import ModelFields
from model_admin.base import model_dc,model_page_dc
from django.contrib.auth.models import Group
import ajax
import json

class UserGroupTable(ModelTable):
    model=Group
    include=['name']


class UserGroupFields(ModelFields):
    template='user_admin/permit.html'
    class Meta:
        model=Group
        fields=['name',]
        
    # def get_heads(self):
        # heads = super(UserGroupFields,self).get_heads()
        # for head in heads:
            # if head['name']==:
                # head['size']=20
        # return heads
    def get_context(self):
        ctx = super(UserGroupFields,self).get_context()
        group = self.instance
        #if not hasattr(group,'permitmodel'):
            #group.permitmodel=PermitModel.objects.create(group=group)
        if hasattr(group,'permitmodel') and group.permitmodel.permit:
            ctx['permits']=json.loads(group.permitmodel.permit) #[{'model':x.model,'permit': json.loads(x.permit)} for x in self.instance.per.all()]
        else:
            ctx['permits']={}
        #ls = []
        ## for k1,v1 in apps.all_models.items():
            ## for k2,v2 in v1.items():
                ## ls.append({'name':'%s.%s'%(k1,k2),'label':'%s.%s'%(k1,k2)})
        #for v in permit_list:
            #if not isinstance(v,dict) and issubclass(v,models.Model):
                #ls.append({'name':model_to_name(v),'label':v._meta.verbose_name})
            ##model = v.get('model')
            ##if model:
                ##ls.append({'name':k,'label':v.get('label',k)})
        #ctx['model_permits']=ls
        
        ctx['permit_heads']=self.permit.get_heads()
        
        return ctx

class GroupTablePage(TablePage):
    tableCls=UserGroupTable

class GroupFormPage(FormPage):
    template='user_admin/permit.html'
    fieldsCls=UserGroupFields
    ajax_scope=ajax.get_globe()

model_dc[Group]={'fields':UserGroupFields}
model_page_dc['group']={'table':GroupTablePage,'form':GroupFormPage,}
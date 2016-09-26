from django.contrib import admin
from models import BasicInfo,MM,Fore

from core.model_render import model_dc
from core.tabel import ModelTable
from core.fields import ModelFields
# Register your models here.
# class BasicAdmin(admin.ModelAdmin):
admin.site.register(BasicInfo)
admin.site.register(MM)
admin.site.register(Fore)


class BasicInfoTable(ModelTable):
    model = BasicInfo
    filters=['name','age']
    include = ['name','age']
    sortable=['age']
    per_page=2
    search_fields=['age','name']


class BasicInfoFields(ModelFields):
    model=BasicInfo
    fields=['name','age','user']
    
    #def get_heads(self):
        #heads = super(BasicInfoFields,self).get_heads()
        #for k in heads:
            #if k['name']=='user':
                #k['type']='sim_select'
        #return heads

model_dc['basicinfo'] ={'model':BasicInfo,'table':BasicInfoTable,'fields':BasicInfoFields}

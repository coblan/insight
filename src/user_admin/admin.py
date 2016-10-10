from django.contrib import admin
from models import BasicInfo,MM,Fore

from core.model_render import model_dc
from core.tabel import ModelTable
from core.fields import ModelFields
from django.contrib.auth.models import User

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
    
    class Meta:
        model=BasicInfo
        fields=['name','age','user'] 
    
    def get_fields(self):
        return ['name','user','age']
    
    def clean_name(self):
        print('here')
        return self.cleaned_data['name']
        
        
class UserTable(ModelTable):
    model=User
    include=['username','first_name']

class UserFields(ModelFields):
    class Meta:
        model=User
        fields=['username','first_name']

model_dc['basicinfo'] ={'model':BasicInfo,'table':BasicInfoTable,'fields':BasicInfoFields}
model_dc['user'] = {'model':User,'table':UserTable,'fields':UserFields}

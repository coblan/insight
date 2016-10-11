# encoding:utf-8
from __future__ import unicode_literals
from django import forms
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
    
    def get_heads(self):
        heads = super(UserTable,self).get_heads()
        heads.extend([{'name':'age','label':'年龄'},
                      {'name':'_name','label':'姓名'}])
        return heads
    
    def get_rows(self):
        rows=super(UserTable,self).get_rows()
        for user_dc in rows:
            user = User.objects.get(pk=user_dc['pk'])
            user_dc['age']=user.basicinfo.age
            user_dc['_name']=user.basicinfo.name
        return rows

class UserFields(ModelFields):
    age = forms.CharField()
    
    def __init__(self,*args,**kw):
        super(UserFields,self).__init__(*args,**kw)
        self.fields.pop('age')
        
    
    class Meta:
        model=User
        fields=['username','first_name']
    
    def get_row(self):
        row = super(UserFields,self).get_row()
        user = User.objects.get(pk= row['pk'])
        row['age']=user.basicinfo.age
        return row
    
    def get_heads(self):
        heads= super(UserFields,self).get_heads()
        for item in heads:
            if item['name']=='age':
                item['type']='text'
        return heads
    
    def clean_age(self):
        print('in age function')
        return self.cleaned_data['age']
    
    def save(self, instane, row):
        user = instane
        user.basicinfo.age=row.get('age')
        user.save()
        user.basicinfo.save()
        return {'status':'success'}
        
    
    
    

model_dc['basicinfo'] ={'model':BasicInfo,'table':BasicInfoTable,'fields':BasicInfoFields}
model_dc['user'] = {'model':User,'table':UserTable,'fields':UserFields}

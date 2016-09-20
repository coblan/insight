from django.contrib import admin
from models import BasicInfo

from core.model_render import model_dc
from core.tabel import ModelTable
from core.fields import ModelFields
# Register your models here.
# class BasicAdmin(admin.ModelAdmin):
admin.site.register(BasicInfo)


class BasicInfoTable(ModelTable):
    model = BasicInfo
    filters=['name','age']
    include = ['name','age']


class BasicInfoFields(ModelFields):
    model=BasicInfo
    fields=['name','age']

model_dc['basicinfo'] ={'model':BasicInfo,'table':BasicInfoTable,'fields':BasicInfoFields}

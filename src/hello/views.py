# encoding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
#from core.model_render import Render
from scheme import menus
from django.contrib.auth.decorators import login_required
from helpers.director.container import evalue_container
from scheme import menus
import json
# from core.port import jsonpost
# Create your views here.

from helpers.pageadaptor.models import WebPage

from engin_proxy import InsightEngine

insight_engine=InsightEngine()

def insight_engine_view(request,name):
    return insight_engine.view(request, name)

def home(request):
    try:
        page = WebPage.objects.get(name='home')
        ctx_dict=json.loads(page.content)
        return render(request,'home.html',context={'menu':evalue_container(menus,user=request.user),'ctx':ctx_dict})
    except WebPage.DoesNotExist:
        return render(request,'home.html',context={'menu':evalue_container(menus,user=request.user)})

#@login_required
#def model_render_views(request,url):
    #md_render=Render(request, url, 
                     #table_temp='model.html', 
                     #fields_temp='fields.html',
                     #del_rows_temp='del_rows.html',
                     #menu=menus)
    ## todo 加入 menu
    ##md_render.
    #return md_render.rout()

    # if request.method=='GET':
        # return rout(request, url, table_temp='model.html', fields_temp='fields.html')
    # else:
        # return jsonpost(request, get_globe())

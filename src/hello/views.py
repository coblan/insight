# encoding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
#from core.model_render import Render
from scheme import menus
from django.contrib.auth.decorators import login_required
from director.container import evalue_container
from scheme import menus
# from core.port import jsonpost
# Create your views here.

def home(request):
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

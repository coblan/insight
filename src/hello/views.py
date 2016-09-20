from django.shortcuts import render
from django.http import HttpResponse
from core.model_render import Render
# from core.port import jsonpost
# Create your views here.

def home(request):
    return HttpResponse('hello home')

def render(request,url):
    md_render=Render(request, url, table_temp='model.html', fields_temp='fields.html')
    return md_render.rout()

    # if request.method=='GET':
        # return rout(request, url, table_temp='model.html', fields_temp='fields.html')
    # else:
        # return jsonpost(request, get_globe())

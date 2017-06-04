from django.shortcuts import render
from helpers.director.port import jsonpost
import ajax
from django.http import HttpResponse
import json
from helpers.common.dir_man import DirMan
from .models import Department2
import inspect
# from core.model_render import render_table
# import admin2
# Create your views here.

# def model_view(request,name):
    # return render_table(request, admin2.get_table_scope(), name, temp='model.html')

def user_admin_ajax(request):
    if request.method=='POST':
        try:
            return jsonpost(request, ajax.get_globe())
        except KeyError as e:
            rt={'status':'error','msg':'key error '+str(e) +' \n may function name error'}
            return HttpResponse(json.dumps(rt),content_type="application/json")    
    
def manage_department(request):
    manager=DirMan(Department2)
    scope= dict(inspect.getmembers(manager,inspect.ismethod))
    return jsonpost(request, scope)
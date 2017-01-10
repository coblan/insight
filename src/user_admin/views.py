from django.shortcuts import render
from helpers.director.port import jsonpost
import ajax
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
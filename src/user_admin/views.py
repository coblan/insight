from django.shortcuts import render
from core.model_render import render_table
import admin2
# Create your views here.

def model_view(request,name):
    return render_table(request, admin2.get_table_scope(), name, temp='model.html')
# encoding:utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

from helpers.director.shortcut import FormPage,TablePage,ModelFields,ModelTable,page_dc,model_dc,permit_list,TabGroup
from helpers.director.db_tools import to_dict
from django.contrib import admin
from .models import EmployeeModel,BasicInfo,Department2
from django.contrib.auth.models import User
from django.db.models import Q
from helpers.common import employee
from helpers.common import department


emp_admin = employee.get_admin(BasicInfo, EmployeeModel)

model_dc[BasicInfo]={'fields': emp_admin['BasicInfoFields']}
model_dc[EmployeeModel]={'fields':emp_admin[ 'EmployeeFields']}

permit_list.append(EmployeeModel)
permit_list.append(BasicInfo)

page_dc.update(emp_admin['engine_dict'])

depart_admin = department.get_admin(Department2)

page_dc.update({
    'department2':depart_admin['DepartmentPage'],
})
model_dc[Department2]={'fields':depart_admin['DepartmentForm']}
permit_list.append(Department2)
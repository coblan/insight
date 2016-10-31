# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-31 08:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0008_auto_20161023_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeinfo',
            name='baseinfo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_admin.BasicInfo'),
        ),
        migrations.AlterField(
            model_name='salaryrecords',
            name='adapt_day',
            field=models.FloatField(blank=True, null=True, verbose_name='\u4fee\u6b63'),
        ),
    ]

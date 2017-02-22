# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-20 09:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0014_auto_20161229_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinfo',
            name='age',
            field=models.CharField(blank=True, max_length=50, verbose_name='age'),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='name',
            field=models.CharField(blank=True, max_length=50, verbose_name='\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='employeemodel',
            name='employ_id',
            field=models.CharField(max_length=50, unique=True, verbose_name='\u804c\u5458ID'),
        ),
    ]
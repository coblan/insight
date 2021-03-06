# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-10 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0021_department_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicinfo',
            name='address',
            field=models.CharField(blank=True, max_length=500, verbose_name='address'),
        ),
        migrations.AddField(
            model_name='basicinfo',
            name='gen',
            field=models.CharField(blank=True, max_length=30, verbose_name='gen'),
        ),
        migrations.AddField(
            model_name='basicinfo',
            name='id_number',
            field=models.CharField(blank=True, max_length=200, verbose_name='id  number'),
        ),
        migrations.AddField(
            model_name='basicinfo',
            name='phone',
            field=models.CharField(blank=True, max_length=100, verbose_name='phone'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-03 14:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import helpers.director.model_validator


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0023_auto_20170603_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='new department', max_length=500, validators=[helpers.director.model_validator.has_str], verbose_name='department name')),
                ('detail', models.TextField(blank=True, verbose_name='\u8be6\u7ec6')),
                ('par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='user_admin.Department2', verbose_name='parent department')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='address',
            field=models.CharField(blank=True, max_length=500, verbose_name='\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='gen',
            field=models.CharField(blank=True, choices=[('male', '\u7537'), ('femal', '\u5973')], max_length=30, verbose_name='\u6027\u522b'),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='head',
            field=models.CharField(blank=True, default='/static/res/image/user.jpg', max_length=200, verbose_name='\u5934\u50cf'),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='id_number',
            field=models.CharField(blank=True, max_length=200, verbose_name='\u8eab\u4efd\u8bc1'),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='name',
            field=models.CharField(blank=True, max_length=50, verbose_name='\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='phone',
            field=models.CharField(blank=True, max_length=100, verbose_name='\u7535\u8bdd'),
        ),
        migrations.AlterField(
            model_name='employeemodel',
            name='eid',
            field=models.CharField(default='', max_length=30, verbose_name='\u5458\u5de5\u53f7'),
        ),
        migrations.AlterField(
            model_name='employeemodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u8d26\u53f7'),
        ),
    ]

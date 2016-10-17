# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-17 15:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0006_auto_20161013_1737'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employ_id', models.CharField(blank=True, max_length=50, verbose_name='\u804c\u5458ID')),
                ('position', models.CharField(blank=True, max_length=100, verbose_name='\u804c\u4f4d')),
                ('salary_level', models.FloatField(blank=True, max_length=100, verbose_name='\u5de5\u8d44')),
                ('baseinfo', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_admin.BasicInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workdays', models.FloatField(blank=True, verbose_name='\u5e94\u8be5\u5de5\u4f5c\u5929\u6570')),
            ],
        ),
        migrations.CreateModel(
            name='SalaryRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_salary', models.FloatField(blank=True, verbose_name='\u57fa\u672c\u5de5\u8d44')),
                ('merit_pay', models.FloatField(blank=True, verbose_name='\u7ee9\u6548\u5de5\u8d44')),
                ('allowance', models.FloatField(blank=True, verbose_name='\u8865\u8d34')),
                ('social_security', models.FloatField(blank=True, verbose_name='\u793e\u4fdd')),
                ('reserved_funds', models.FloatField(blank=True, verbose_name='\u793e\u4fdd')),
                ('adapt_day', models.FloatField(blank=True, verbose_name='\u4fee\u6b63')),
                ('empoyee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_admin.EmployeeInfo', verbose_name='\u5458\u5de5')),
                ('month', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_admin.Month', verbose_name='\u6708\u4efd')),
            ],
        ),
    ]

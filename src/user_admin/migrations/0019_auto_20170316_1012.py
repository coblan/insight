# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-03-16 02:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0018_salaryrecords_is_checked'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='department name')),
                ('detail', models.TextField(blank=True, verbose_name='\u8be6\u7ec6')),
                ('sub_depart', models.CharField(blank=True, max_length=500, verbose_name='sub department')),
            ],
        ),
        migrations.AlterField(
            model_name='salaryrecords',
            name='is_checked',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u68c0\u67e5\u8fc7'),
        ),
    ]

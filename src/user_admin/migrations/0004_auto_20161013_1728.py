# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-13 09:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0003_auto_20160925_1935'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basicinfo',
            options={'default_permissions': 'add'},
        ),
    ]

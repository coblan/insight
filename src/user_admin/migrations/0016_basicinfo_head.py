# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-22 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0015_auto_20170220_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicinfo',
            name='head',
            field=models.CharField(blank=True, max_length=200, verbose_name='head image'),
        ),
    ]

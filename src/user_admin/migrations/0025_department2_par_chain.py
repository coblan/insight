# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-04 04:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0024_auto_20170603_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='department2',
            name='par_chain',
            field=models.CharField(blank=True, max_length=200, verbose_name='parent chain'),
        ),
    ]

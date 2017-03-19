# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-19 09:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0019_auto_20170316_1012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='sub_depart',
        ),
        migrations.AddField(
            model_name='department',
            name='par',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_dep', to='user_admin.Department', verbose_name='parent department'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-04 06:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0010_auto_20161103_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permitmodel',
            name='model',
        ),
        migrations.AlterField(
            model_name='permitmodel',
            name='group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.Group', verbose_name='group'),
        ),
        migrations.AlterField(
            model_name='permitmodel',
            name='permit',
            field=models.TextField(default='[]', verbose_name='permit'),
        ),
    ]
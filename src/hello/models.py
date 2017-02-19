from __future__ import unicode_literals

from django.db import models

# Create your models here.

class KVModel(models.Model):
    key=models.CharField('key',max_length=300)
    value=models.TextField(verbose_name='value',blank=True)

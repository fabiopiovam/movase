# -*- coding: utf-8 -*-

from django.db import models

class Imports(models.Model):
    url         = models.CharField(max_length=100)
    imported_at = models.DateTimeField(auto_now_add=True)
    total       = models.IntegerField()
    imported    = models.IntegerField()
    errors      = models.IntegerField()
    
class ImportItems(models.Model):
    imports     = models.ForeignKey(Imports)
    identifier  = models.CharField(max_length=100)
    title       = models.CharField(max_length=100)
    imported    = models.BooleanField(default=False)
    message     = models.CharField(max_length=200)
# -*- coding: utf-8 -*-

from django.db import models

class Log(models.Model):
    url         = models.CharField(max_length=100)
    imported_at = models.DateTimeField(auto_now_add=True)
    total       = models.IntegerField(default=0)
    imported    = models.IntegerField(default=0)
    errors      = models.IntegerField(default=0)
    message     = models.CharField(max_length=200)
    
class LogItem(models.Model):
    log         = models.ForeignKey(Log)
    identifier  = models.CharField(max_length=100)
    title       = models.CharField(max_length=100)
    imported    = models.BooleanField(default=False)
    message     = models.CharField(max_length=200)
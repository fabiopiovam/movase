# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from adminsortable.models import Sortable

class Category(models.Model):
    
    def __unicode__(self):
        return u'%s' % self.title
    
    class Meta:
        verbose_name = u"categoria"
        ordering = ('title',)
    
    def save(self, *args, **kwargs):
        if not self.id:
            super(Category, self).save(*args, **kwargs)
            self.slug = slugify(self.title.strip())
        super(Category, self).save(*args, **kwargs)
    
    title = models.CharField(u'Categoria', max_length=80)
    slug  = models.SlugField(max_length=100, unique=True)

class Link(Sortable):
    
    def __unicode__(self):
        return u'%s' % self.title
    
    category    = models.ForeignKey(Category, verbose_name=u"Categoria", null=True, blank=True)
    title       = models.CharField(u'Título', max_length=100)
    description = models.CharField(u'Descrição', null=True, blank=True, max_length=200)
    url         = models.URLField(u'URL')
    target_blank= models.BooleanField(u'Abrir em nova janela')

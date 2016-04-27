# -*- coding: utf-8 -*-

from django.contrib import admin

from adminsortable.admin import SortableAdmin

from models import Category, Link

class LinkAdmin(SortableAdmin):
    list_display = ('title','url')
    search_fields = ['title','url']
    list_filter = ['category__title']
    # fields = ('title',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ['title', 'slug']
    fields = ('title',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Link, LinkAdmin)

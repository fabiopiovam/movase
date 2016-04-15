# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from models import Page

class LastArticles(Feed):
    title = 'Ultimas publicações'
    link = '/'
    description = "Fique por dentro das ultimas atualizações"

    def items(self):
        return Page.objects.all()[:10]

    def item_link(self, item):
        return reverse('page', args=[item.slug])
    
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary
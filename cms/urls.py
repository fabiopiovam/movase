from django.conf.urls import patterns, include, url

from cms.feeds import LastArticles

urlpatterns = patterns('',
    (r'^rss/$', LastArticles()),
)
urlpatterns += patterns('cms.views',
    url(r'^category/(?P<category_slug>.*?)/$', 'pages', name='category'),
    url(r'^$', 'pages', name='pages'),
    url(r'^(?P<slug>.*?)/$', 'page', name='page'),
)
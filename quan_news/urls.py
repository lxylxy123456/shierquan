from django.conf.urls import *
from django.contrib.sitemaps.views import sitemap
from .views import NewsViews, NewsSiteMap

urlpatterns = [
    url(r'^news/$', NewsViews.news_list),
    url(r'^news/post/$', NewsViews.news_post),
    url(r'^news/([0-9]+)/$', NewsViews.news_view),
    url(r'^news/([0-9]+)/delete/$', NewsViews.news_delete),
    url(r'^news/sitemap\.xml$', sitemap, {'sitemaps': { 'news': NewsSiteMap }},
        name='django.contrib.sitemaps.views.sitemap'), 
]

from django.conf.urls import *
from django.contrib.sitemaps.views import sitemap
from .views import ShareViews, ShareSiteMap

urlpatterns = [
    url(r'^create/$', ShareViews.share_create),
    url(r'^upload/$', ShareViews.attach_create),
    url(r'^download/$', ShareViews.attach_download), 
    url(r'^chat/$', ShareViews.chat_create), 
    url(r'^upload/complete/$', ShareViews.uuid_get), 
    url(r'^upload/progress/$', ShareViews.progress_find), 
    url(r'^([A-Za-z0-9\-]+)/$', ShareViews.share_show),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': { 'share': ShareSiteMap }},
        name='django.contrib.sitemaps.views.sitemap'), 
]

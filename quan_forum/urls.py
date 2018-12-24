from django.conf.urls import *
from django.contrib.sitemaps.views import sitemap
from .views import ForumViews, ForumSiteMap

urlpatterns = [
    url(r'^$', ForumViews.forum_show), 
    url(r'^([A-Za-z\-]+)/$', ForumViews.group_show), 
    url(r'^([A-Za-z\-]+)/post/$', ForumViews.thread_post), 
    url(r'^([A-Za-z\-]+)/edit/$', ForumViews.thread_post), 
    url(r'^([A-Za-z\-]+)/([0-9]+)/$', ForumViews.thread_show), 
    url(r'^([A-Za-z\-]+)/([0-9]+)/post/$', ForumViews.thread_post), 
    url(r'^([A-Za-z\-]+)/([0-9]+)/edit/$', ForumViews.thread_post), 
    url(r'^([A-Za-z\-]+)/([0-9]+)/chat/$', ForumViews.thread_chat), 
    url(r'^([A-Za-z\-]+)/delete/$', ForumViews.forum_delete), 
    # 以下链接由于包含字母，所以不会和上面的冲突
    url(r'^special/random/$', ForumViews.random), 
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': { 'forum': ForumSiteMap }},
        name='django.contrib.sitemaps.views.sitemap'), 
]

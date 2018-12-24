from django.conf.urls import *
from .views import ForumViewsOld

urlpatterns = [
    url(r'^$', ForumViewsOld.forum_show), 
    url(r'^([A-Za-z\-]+)/$', ForumViewsOld.group_show), 
    url(r'^([A-Za-z\-]+)/post/$', ForumViewsOld.thread_post), 
    url(r'^([A-Za-z\-]+)/edit/$', ForumViewsOld.thread_post), 
    url(r'^([A-Za-z\-]+)/([0-9]+)/$', ForumViewsOld.thread_show), 
    url(r'^([A-Za-z\-]+)/([0-9]+)/post/$', ForumViewsOld.thread_post), 
    url(r'^([A-Za-z\-]+)/([0-9]+)/edit/$', ForumViewsOld.thread_post), 
    url(r'^([A-Za-z\-]+)/delete/$', ForumViewsOld.forum_delete), 
    # 以下链接由于包含字母，所以不会和上面的冲突
    url(r'^special/random/$', ForumViewsOld.random), 
#    url(r'^([A-Za-z\-]+)/delete/$', ForumViewsOld.group_delete), 
#    url(r'^([A-Za-z\-]+)/([0-9]+)/delete/$', ForumViewsOld.thread_delete), 
]

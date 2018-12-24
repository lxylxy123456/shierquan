from django.conf.urls import *
from .views import UserAgentViews

urlpatterns = [
    url(r'^api/$', UserAgentViews.api),
    url(r'^robots.txt$', UserAgentViews.robots), 
    url(r'^googlec5839a5189511839.html$', UserAgentViews.robots), 
    url(r'^baidu_verify_fRfpbKd9Y2.html$', UserAgentViews.robots), 
    url(r'^shierquan-sitemap\.xml$', UserAgentViews.robots), 
]

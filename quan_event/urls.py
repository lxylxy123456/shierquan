from django.conf.urls import *
from django.contrib.sitemaps.views import sitemap
from .views import EventViews, EventSiteMap

urlpatterns = [
    url(r'^nice/$', EventViews.event_nice),
    url(r'^follow/$', EventViews.event_follow),
    url(r'^create/$', EventViews.event_create),
    url(r'^create/(history)/$', EventViews.event_create),
    url(r'^cancel/$', EventViews.event_cancel),
    url(r'^(\d{1,8})/$', EventViews.event_show),
    url(r'^latest/$', EventViews.event_latest),
    url(r'^next/$', EventViews.event_next),
    url(r'^(\d{1,8})/manual/$', EventViews.event_manual),
    url(r'^(\d{1,8})/relate/$', EventViews.event_share_relate),
    url(r'^signup/submit/$', EventViews.event_signup_submit),
    url(r'^signup/qrcode/$', EventViews.event_signup_qrcode),
    url(r'^signup/create/$', EventViews.event_signup_create),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': { 'event': EventSiteMap }},
        name='django.contrib.sitemaps.views.sitemap'), 
]

from django.conf.urls import *
from .views import BadgeViews

urlpatterns = [
    url(r'^create/$', BadgeViews.badge_create),
    url(r'^grant/$', BadgeViews.badge_grant),
    url(r'^list/$', BadgeViews.badge_list),
    url(r'^remove/$', BadgeViews.badge_remove),
    url(r'^withdraw/$', BadgeViews.badge_withdraw),
]

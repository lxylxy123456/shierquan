from django.conf.urls import *
from .views import MobileViews

urlpatterns = [
    url(r'^club/$', MobileViews.clublist_find), 
    url(r'^save/$', MobileViews.host_id_save), 
    url(r'^host/$', MobileViews.host_id_find), 
    url(r'^privacy/$', MobileViews.privacy), 
]

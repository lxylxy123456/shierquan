from django.conf.urls import *
from .views import AuthViews

urlpatterns = [
    url(r'^apply/$', AuthViews.auth_apply), 
    url(r'^apply/rubric/([A-Za-z\-]+)/$', AuthViews.auth_apply_rubric), 
    url(r'^edit/$', AuthViews.auth_manage), 
    url(r'^room/$', AuthViews.room_apply), 
    url(r'^batch/$', AuthViews.batch), 
    url(r'^empty/([A-Za-z\-]+)/$', AuthViews.empty_view), 
    url(r'^funds/$', AuthViews.funds_all), 
    url(r'^funds/show/(\d{1,10})/$', AuthViews.funds_show), 
    url(r'^funds/modify/(\d{1,10})/$', AuthViews.funds_apply), 
    url(r'^funds/delete/(\d{1,10})/$', AuthViews.funds_delete), 
    url(r'^funds/download/(\d{1,10})/$', AuthViews.funds_download), 
    url(r'^funds/([A-Za-z\-]+)/list/$', AuthViews.funds_list), 
    url(r'^funds/([A-Za-z\-]+)/(apply)/$', AuthViews.funds_apply), 
]

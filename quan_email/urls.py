from django.conf.urls import *
from .views import EmailViews

urlpatterns = [
    url(r'^reset/$', EmailViews.password_reset),
    url(r'^reset/([0-9a-f]+)/$', EmailViews.password_set),
    url(r'^global/$', EmailViews.global_email),
]

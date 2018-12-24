from django.conf.urls import *
from .views import MessageViews

urlpatterns = [
    url(r'^global/$', MessageViews.global_message_fetch), 
    url(r'^private/$', MessageViews.private_message_fetch), 
    url(r'^hi/$', MessageViews.contact_hi), 
    url(r'^send/$', MessageViews.message_send), 
    url(r'^leave/$', MessageViews.message_leave), 
]

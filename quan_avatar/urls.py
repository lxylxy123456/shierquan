from django.conf.urls import *
from .views import AvatarViews

urlpatterns = [
    url(r'^(user)/([A-Za-z\-]+)/$', AvatarViews.avatar_upload),
    url(r'^(club)/([A-Za-z\-]+)/$', AvatarViews.avatar_upload),
    url(r'^(forum)/([A-Za-z\-]+)/$', AvatarViews.avatar_upload),
]

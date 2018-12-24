from django.conf.urls import *
from .views import AccountViews

urlpatterns = [
    url(r'^signup/$', AccountViews.user_signup),
    url(r'^login/$', AccountViews.user_login),
    url(r'^logout/$', AccountViews.user_logout),
    url(r'^create/$', AccountViews.club_create),
    url(r'^club/([A-Za-z\-]+)/follow/$', AccountViews.club_follow),
    url(r'^club/([A-Za-z\-]+)/join/$', AccountViews.club_join),
    url(r'^club/([A-Za-z\-]+)/edit/$', AccountViews.club_edit),
    url(r'^club/([A-Za-z\-]+)/alias/$', AccountViews.club_alias),
    url(r'^user/([A-Za-z\-]+)/edit/$', AccountViews.user_edit),
    url(r'^user/([A-Za-z\-]+)/reset/$', AccountViews.reset_password),
    url(r'^account/nickname/$', AccountViews.nickname),
    url(r'^follow/user/$', AccountViews.user_follow),
    url(r'^friend/user/$', AccountViews.user_friend),
    url(r'^search/(user)/$', AccountViews.account_search),
    url(r'^search/(all)/$', AccountViews.account_search),
    url(r'^search/(club)/$', AccountViews.account_search),
    url(r'^api/login/$', AccountViews.api_user_login),
]

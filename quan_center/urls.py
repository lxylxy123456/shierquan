from django.conf.urls import *
from django.contrib.sitemaps.views import sitemap
from .views import CenterViews, ClubSiteMap, UserSiteMap

urlpatterns = [
    url(r'^club/([A-Za-z\-]+)/$', CenterViews.club_show),
    url(r'^club/([A-Za-z\-]+)/manage/$', CenterViews.member_manage),
    url(r'^club/([A-Za-z\-]+)/alter/$', CenterViews.member_set),
    url(r'^club/([A-Za-z\-]+)/follower/$', CenterViews.follower_list),
    url(r'^(club)/([A-Za-z\-]+)/detail/$', CenterViews.detail), 
    url(r'^(user)/([A-Za-z\-]+)/detail/$', CenterViews.detail), 
    url(r'^user/$', CenterViews.user_redirect), 
    url(r'^user/([A-Za-z\-]+)/$', CenterViews.user_show), 
    url(r'^user/([A-Za-z\-]+)/signature/$', CenterViews.signature_modify), 
    url(r'^club/([A-Za-z\-]+)/album/$', CenterViews.album_show),
    url(r'^club/sitemap\.xml$', sitemap, {'sitemaps': { 'club': ClubSiteMap }},
        name='django.contrib.sitemaps.views.sitemap'), 
    url(r'^user/sitemap\.xml$', sitemap, {'sitemaps': { 'user': UserSiteMap }},
        name='django.contrib.sitemaps.views.sitemap'), 
]

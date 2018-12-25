# 
# Shierquan - a website similar to shiyiquan.net; see README.md
# Copyright (C) 2018  lxylxy123456
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# 

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

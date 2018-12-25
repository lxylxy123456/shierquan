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

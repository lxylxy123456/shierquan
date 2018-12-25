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
from .views import EventViews, EventSiteMap

urlpatterns = [
    url(r'^nice/$', EventViews.event_nice),
    url(r'^follow/$', EventViews.event_follow),
    url(r'^create/$', EventViews.event_create),
    url(r'^create/(history)/$', EventViews.event_create),
    url(r'^cancel/$', EventViews.event_cancel),
    url(r'^(\d{1,8})/$', EventViews.event_show),
    url(r'^latest/$', EventViews.event_latest),
    url(r'^next/$', EventViews.event_next),
    url(r'^(\d{1,8})/manual/$', EventViews.event_manual),
    url(r'^(\d{1,8})/relate/$', EventViews.event_share_relate),
    url(r'^signup/submit/$', EventViews.event_signup_submit),
    url(r'^signup/qrcode/$', EventViews.event_signup_qrcode),
    url(r'^signup/create/$', EventViews.event_signup_create),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': { 'event': EventSiteMap }},
        name='django.contrib.sitemaps.views.sitemap'), 
]

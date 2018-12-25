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
from .views import ForumViews, ForumSiteMap

urlpatterns = [
    url(r'^$', ForumViews.forum_show), 
    url(r'^([A-Za-z\-]+)/$', ForumViews.group_show), 
    url(r'^([A-Za-z\-]+)/post/$', ForumViews.thread_post), 
    url(r'^([A-Za-z\-]+)/edit/$', ForumViews.thread_post), 
    url(r'^([A-Za-z\-]+)/([0-9]+)/$', ForumViews.thread_show), 
    url(r'^([A-Za-z\-]+)/([0-9]+)/post/$', ForumViews.thread_post), 
    url(r'^([A-Za-z\-]+)/([0-9]+)/edit/$', ForumViews.thread_post), 
    url(r'^([A-Za-z\-]+)/([0-9]+)/chat/$', ForumViews.thread_chat), 
    url(r'^([A-Za-z\-]+)/delete/$', ForumViews.forum_delete), 
    # 以下链接由于包含字母，所以不会和上面的冲突
    url(r'^special/random/$', ForumViews.random), 
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': { 'forum': ForumSiteMap }},
        name='django.contrib.sitemaps.views.sitemap'), 
]

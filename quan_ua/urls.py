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
from .views import UserAgentViews

urlpatterns = [
    url(r'^api/$', UserAgentViews.api),
    url(r'^robots.txt$', UserAgentViews.robots), 
    url(r'^googlec5839a5189511839.html$', UserAgentViews.robots), 
    url(r'^baidu_verify_fRfpbKd9Y2.html$', UserAgentViews.robots), 
    url(r'^shierquan-sitemap\.xml$', UserAgentViews.robots), 
]

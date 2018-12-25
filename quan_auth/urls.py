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
from .views import AuthViews

urlpatterns = [
    url(r'^apply/$', AuthViews.auth_apply), 
    url(r'^apply/rubric/([A-Za-z\-]+)/$', AuthViews.auth_apply_rubric), 
    url(r'^edit/$', AuthViews.auth_manage), 
    url(r'^room/$', AuthViews.room_apply), 
    url(r'^batch/$', AuthViews.batch), 
    url(r'^empty/([A-Za-z\-]+)/$', AuthViews.empty_view), 
    url(r'^funds/$', AuthViews.funds_all), 
    url(r'^funds/show/(\d{1,10})/$', AuthViews.funds_show), 
    url(r'^funds/modify/(\d{1,10})/$', AuthViews.funds_apply), 
    url(r'^funds/delete/(\d{1,10})/$', AuthViews.funds_delete), 
    url(r'^funds/download/(\d{1,10})/$', AuthViews.funds_download), 
    url(r'^funds/([A-Za-z\-]+)/list/$', AuthViews.funds_list), 
    url(r'^funds/([A-Za-z\-]+)/(apply)/$', AuthViews.funds_apply), 
]

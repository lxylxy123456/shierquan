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
from .views import MessageViews

urlpatterns = [
    url(r'^global/$', MessageViews.global_message_fetch), 
    url(r'^private/$', MessageViews.private_message_fetch), 
    url(r'^hi/$', MessageViews.contact_hi), 
    url(r'^send/$', MessageViews.message_send), 
    url(r'^leave/$', MessageViews.message_leave), 
]

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
from .views import *

urlpatterns = [
    url(r'^$', SquareViews.home_view),
    url(r'^wall/$', SquareViews.wall_view),
    url(r'^search/$', SquareViews.search_view),
    url(r'^search/(event)/$', SquareViews.search_view),
    url(r'^search/(share)/$', SquareViews.search_view),
    url(r'^guide/$', SquareViews.guide_view),
    url(r'^square/$', SquareViews.event_all),
    url(r'^square/relative/$', SquareViews.event_all),
    url(r'^square/hotest/$', SquareViews.event_all),
    url(r'^square/club/$', SquareViews.club_all),
    url(r'^square/club/fetch/$', SquareViews.club_fetch),
    url(r'^home/note-read/$', SquareViews.note_read),
    url(r'^random/$', SquareViews.club_random),
]

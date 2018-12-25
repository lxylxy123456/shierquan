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

from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

handler404 = 'defaults.page_not_found'
handler500 = 'defaults.server_error'
handler403 = 'defaults.permission_denied'
handler400 = 'defaults.bad_request'

admin.site.site_header = '十二圈后台'
admin.site.index_title = '站点管理'

urlpatterns = [
    # Examples:
    # url(r'^$', 'shierquan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^static/(?P<path>.*)$', serve, settings.STATIC_DICT),
    url(r'^media/(?P<path>.*)$', serve, settings.MEDIA_DICT),

    url(r'^', include('quan_account.urls')),
    url(r'^', include('quan_center.urls')),
    url(r'^', include('quan_email.urls')),
    url(r'^', include('quan_square.urls')),
    url(r'^', include('quan_news.urls')),
    url(r'^', include('quan_ua.urls')),

    url(r'^auth/',include('quan_auth.urls')),
    url(r'^avatar/', include('quan_avatar.urls')),
    url(r'^badge/',include('quan_badge.urls')),
    url(r'^event/', include('quan_event.urls')),
    url(r'^message/',include('quan_message.urls')),
    url(r'^share/',include('quan_share.urls')), 
    url(r'^mobile/',include('quan_mobile.urls')), 
    url(r'^forum/', include('quan_forum.urls')), 
    url(r'^forum-old/', include('quan_forum_old.urls')), 

    url(r'^admin/', include(admin.site.urls)),
]


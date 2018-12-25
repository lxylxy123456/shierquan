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

from django.contrib import admin
from .models import *

class GlobalMessage_admin(admin.ModelAdmin) :
	list_display = ('id', 'relation', 'action', 'major_id', 'major_relation', 
					'minor_id', 'minor_relation', 'time_update', 'platform', 
					'data', 'status', )
	search_fields = list_display
	list_filter = ('status', 'relation', 'action', 'time_update', 'data', )

class PrivateMessage_admin(admin.ModelAdmin) :
	list_display = ('id', 'content', 'conn_id', 'conn_relation', 'recv_id', 
					'recv_relation', 'send_id', 'send_relation', 'time_update', 
					'time_create', 'reference', 'status', 'data', 'deleted', )
	search_fields = list_display
	list_filter = ('deleted', 'conn_relation', 'send_relation', 
					'recv_relation', 'status', )

admin.site.register(GlobalMessage, GlobalMessage_admin)
admin.site.register(PrivateMessage, PrivateMessage_admin)


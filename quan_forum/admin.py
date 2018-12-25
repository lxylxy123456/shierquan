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

class ForumGroup_admin(admin.ModelAdmin) :
	list_display = ('id', 'status', 'account_id', 'simp_name', 'subject', 
					'topic', 'secret', 'time_create', )
	search_fields = list_display + ('content', 'time_update', )
	list_filter = ('status', 'secret', 'topic', )

class ForumThread_admin(admin.ModelAdmin) :
	list_display = ('id', 'status', 'send_id', 'subject', 'group_id', 
					'attach_uuid', 'response_number', 'time_create', )
	search_fields = list_display + ('content', 'time_update', )
	list_filter = ('status', 'group_id', )

class ForumResponse_admin(admin.ModelAdmin) :
	list_display = ('id', 'status', 'send_id', 'reply_id', 'reply_relation', 
					'content', 'time_create', 'thread_id', 'attach_uuid', )
	search_fields = list_display + ('time_update', )
	list_filter = ('status', 'reply_relation', 'time_create', )

class ForumHistory_admin(admin.ModelAdmin) :
	list_display = ('id', 'relation', 'account_id', 'subject', 'content', 
					'time_create', )
	search_fields = list_display + ('time_update', )
	list_filter = ('relation', 'time_create', )

admin.site.register(ForumGroup, ForumGroup_admin)
admin.site.register(ForumThread, ForumThread_admin)
admin.site.register(ForumResponse, ForumResponse_admin)
admin.site.register(ForumHistory, ForumHistory_admin)


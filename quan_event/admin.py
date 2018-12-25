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

class EventInfo_admin(admin.ModelAdmin) :
	list_display = ('id', 'subject', 'time_set', 'time_end', 'time_create', 
					'location', 'category', 'account_id', 'relation', 'status', 
					'visitors', )
	search_fields = list_display + ('content', )
	list_filter = ('time_set', 'time_create', 'category', )

class EventQuest_admin(admin.ModelAdmin) :
	list_display = ('id', 'event_id', 'answer', 'quest', 'time_create', 
					'token', )
	search_fields = list_display + ('option_A', 'option_B', 'option_C', )
	list_filter = ('time_create', )

class EventRelation_admin(admin.ModelAdmin) :
	list_display = ('id', 'account_id', 'relation', 'event_id', 'status', 
					'time_create', )
	search_fields = list_display
	list_filter = ('status', 'time_create', )

class ShareEventRelation_admin(admin.ModelAdmin) :
	list_display = ('id', 'share_id', 'event_id', 'time_create', 'time_update', 
					'status', )
	search_fields = list_display
	list_filter = ('status', 'time_create', 'time_update', )

admin.site.register(EventInfo, EventInfo_admin)
admin.site.register(EventQuest, EventQuest_admin)
admin.site.register(EventRelation, EventRelation_admin)
admin.site.register(ShareEventRelation, ShareEventRelation_admin)


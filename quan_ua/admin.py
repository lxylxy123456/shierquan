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

class UserAgentInfo_admin(admin.ModelAdmin) :
	list_display = ('id', 'simp_name', 'ipaddr', 'method', 'path', 'agent', 
					'time_create', 'host', 'status_code')	# 列表显示
	search_fields = list_display							# 搜索
	list_filter = ()					# 禁止过滤，因为可能造成服务器负载增加
		# 例如在 20170302 ，过滤 method 和 time_create 导致了服务器相应近 10 秒

class RealNameInfo_admin(admin.ModelAdmin) :
	list_display = ('id', 'name', 'status', 'used', 'account_id', 
					'time_update', )
	search_fields = list_display
	list_filter = ('status', 'used', )

admin.site.register(UserAgentInfo, UserAgentInfo_admin)
admin.site.register(RealNameInfo, RealNameInfo_admin)


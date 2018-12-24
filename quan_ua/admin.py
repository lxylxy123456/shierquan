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


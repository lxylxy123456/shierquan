from django.contrib import admin
from .models import *

class BadgeInfo_admin(admin.ModelAdmin) :
	list_display = ('id', 'name', 'desc', 'rank', 'account_id', 'category', 
					'status', 'time_update', 'time_create', )
	search_fields = list_display
	list_filter = ('rank', 'category', 'status', 'time_create', )

class BadgeRelation_admin(admin.ModelAdmin) :
	list_display = ('id', 'badge_id', 'reason', 'send_id', 'recv_id', 'data', 
					'time_update', )
	search_fields = list_display
	list_filter = ('time_update', )

admin.site.register(BadgeInfo, BadgeInfo_admin)
admin.site.register(BadgeRelation, BadgeRelation_admin)


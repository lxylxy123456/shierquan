from django.contrib import admin
from .models import *

class ShareInfo_admin(admin.ModelAdmin) :
	list_display = ('id', 'status', 'subject', 'time_update', 'time_create', 						'account_id', 'relation', 'attach_uuid', 'category', 
					'password', 'visitors', )
	search_fields = list_display + ('content', )
	list_filter = ('status', 'category', 'relation', )

class ShareAttach_admin(admin.ModelAdmin) :
	list_display = ('id', 'shared', 'attach_uuid', 'second_uuid', 'category', 
					'name_new', 'name_raw', 'description', 'account_id', 
					'relation', 'time_create', 'downloads', 'size', 
					'video_status', 'video_height', 'video_width', 
					'mp4_status', 'webm_status', )
	search_fields = list_display
	list_filter = ('shared', 'category', 'video_status', )

admin.site.register(ShareInfo, ShareInfo_admin)
admin.site.register(ShareAttach, ShareAttach_admin)


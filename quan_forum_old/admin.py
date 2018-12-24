from django.contrib import admin
from .models import *

class ForumGroupOld_admin(admin.ModelAdmin) :
	list_display = ('id', 'status', 'account_id', 'simp_name', 'subject', 
					'topic', 'secret', 'time_create', )
	search_fields = list_display + ('content', 'time_update', )
	list_filter = ('status', 'secret', 'topic', )

class ForumThreadOld_admin(admin.ModelAdmin) :
	list_display = ('id', 'status', 'send_id', 'subject', 'group_id', 
					'attach_uuid', 'response_number', 'time_create', )
	search_fields = list_display + ('content', 'time_update', )
	list_filter = ('status', 'group_id', )

class ForumResponseOld_admin(admin.ModelAdmin) :
	list_display = ('id', 'status', 'send_id', 'reply_id', 'reply_relation', 
					'content', 'time_create', 'thread_id', 'attach_uuid', )
	search_fields = list_display + ('time_update', )
	list_filter = ('status', 'reply_relation', 'time_create', )

class ForumHistoryOld_admin(admin.ModelAdmin) :
	list_display = ('id', 'relation', 'account_id', 'subject', 'content', 
					'time_create', )
	search_fields = list_display + ('time_update', )
	list_filter = ('relation', 'time_create', )

admin.site.register(ForumGroupOld, ForumGroupOld_admin)
admin.site.register(ForumThreadOld, ForumThreadOld_admin)
admin.site.register(ForumResponseOld, ForumResponseOld_admin)
admin.site.register(ForumHistoryOld, ForumHistoryOld_admin)


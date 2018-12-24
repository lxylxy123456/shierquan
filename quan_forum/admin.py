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


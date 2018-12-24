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


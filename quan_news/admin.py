from django.contrib import admin
from .models import *

class NewsInfo_admin(admin.ModelAdmin) :
	list_display = ('id', 'subject', 'time_update', 'account_id', 'relation', 
					'attach_uuid', 'category', 'status', 'visited', )
	search_fields = list_display + ('content', )
	list_filter = ('status', 'relation', 'time_update', 'category', )

admin.site.register(NewsInfo, NewsInfo_admin)


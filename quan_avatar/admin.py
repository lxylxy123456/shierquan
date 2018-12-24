from django.contrib import admin
from .models import *

class AvatarAccount_admin(admin.ModelAdmin) :
	list_display = ('id', 'name', 'temp_name', 'account_id', 'relation', 
					'time_update', )
	search_fields = list_display
	list_filter = ('relation', 'time_update', )

class AvatarTemp_admin(admin.ModelAdmin) :
	list_display = ('id', 'image', 'raw_name', 'account_id', 'relation', 
					'time_update', )
	search_fields = list_display
	list_filter = ('relation', 'time_update', )

admin.site.register(AvatarAccount, AvatarAccount_admin)
admin.site.register(AvatarTemp, AvatarTemp_admin)


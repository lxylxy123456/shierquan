from django.contrib import admin
from .models import *

class UpdateStatus_admin(admin.ModelAdmin) :
	list_display = ('id', 'category', 'account_id', 'relation', 'hash_value', 
					'time_update', 'time_create', )
	search_fields = list_display + ('content', )
	list_filter = ('category', 'time_create', )

admin.site.register(UpdateStatus, UpdateStatus_admin)


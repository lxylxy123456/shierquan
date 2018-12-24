from django.contrib import admin
from .models import *

class AuthInfo_admin(admin.ModelAdmin) :
	list_display = ('id', 'account_id', 'relation', 'data', 'stars', 
					'time_update', 'time_create', )
	search_fields = list_display + ('extra', 'score', )
	list_filter = ('relation', 'stars', 'time_update', 'time_create', )

admin.site.register(AuthInfo, AuthInfo_admin)


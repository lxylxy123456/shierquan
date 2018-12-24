from django.contrib import admin
from .models import *

class MobileHost_admin(admin.ModelAdmin) :
	list_display = ('id', 'account_id', 'host_id', 'time_create', )
	search_fields = list_display
	list_filter = ('time_update', )

admin.site.register(MobileHost, MobileHost_admin)


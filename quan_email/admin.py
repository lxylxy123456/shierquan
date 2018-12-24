from django.contrib import admin
from .models import *

class EmailInfo_admin(admin.ModelAdmin) :
	list_display = ('id', 'subject', 'reciever', 'subtype', 'charset', 
					'status', 'category', 'account_id', 'relation', 
					'time_create', )
	search_fields = list_display + ('content', )
	list_filter = ('category', 'subtype', 'time_create', )

admin.site.register(EmailInfo, EmailInfo_admin)


from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserAccount_admin(admin.ModelAdmin) :
	list_display = ('id', 'basic', 'grade', 'phone', 'nickname', )
	search_fields = ('id', 'grade', 'phone', 'nickname', )
	list_filter = ('grade', )

class ClubAccount_admin(admin.ModelAdmin) :
	list_display = ('id', 'full_name', 'simp_name', 'category', 'simp_intro', 
					'time_create', 'time_update', )
	search_fields = list_display
	list_filter = ('category', 'time_create', )

class CustomUser_admin(UserAdmin) :
	list_display = ('id', 'username', 'first_name', 'last_name', 
					'is_active', 'is_staff', )
	search_fields = list_display

class ClubAlias_admin(admin.ModelAdmin) :
	list_display = ('id', 'status', 'club_id', 'alias', 'time_create', 
					'time_update', )
	search_fields = list_display
	list_filter = ('status', 'time_create', )

class AccountRelation_admin(admin.ModelAdmin) :
	list_display = ('id', 'account_id_A', 'account_id_B', 'relation', 'data', 
					'time_create', 'time_update', )
	search_fields = list_display
	list_filter = ('relation', 'time_create', )

admin.site.unregister(User)
admin.site.register(User, CustomUser_admin)
admin.site.register(UserAccount, UserAccount_admin)
admin.site.register(ClubAccount, ClubAccount_admin)
admin.site.register(ClubAlias, ClubAlias_admin)
admin.site.register(AccountRelation, AccountRelation_admin)


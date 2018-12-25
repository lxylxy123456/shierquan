# 
# Shierquan - a website similar to shiyiquan.net; see README.md
# Copyright (C) 2018  lxylxy123456
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# 

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


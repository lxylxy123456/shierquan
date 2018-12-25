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


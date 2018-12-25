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

from common import *

class MobileHost(models.Model):
	account_id = models.IntegerField(u'用户ID', default=0)
	host_id = models.CharField(u'机主ID', default='', max_length=100, unique=True)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	
	allowed_keys = ()

	class Meta:
		db_table = 'MobileHost'
		verbose_name = verbose_name_plural = '移动端' + keep_en(db_table)


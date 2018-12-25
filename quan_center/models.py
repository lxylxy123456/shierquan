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

class UpdateStatus(models.Model) :
	'''
		储存用户或社团的历史信息
		说明:
			relation	|	category
			------------+---------------
			user		|	signature
			user		|	nickname
			club		|	simp_intro
			club		|	full_intro
	'''
	content = models.CharField(u'内容', default='', max_length=1200)
	category = models.CharField(u'更新类型', default='', max_length=120)
	account_id = models.IntegerField(u'ID', default=0)
	relation = models.CharField(u'关系', default='', max_length=120)
	hash_value = models.IntegerField(u'哈希', default=0)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	
	allowed_keys = ('id', 'content', 'category')
	
	class Meta:
		db_table = 'UpdateStatus'
		verbose_name = verbose_name_plural = '介绍更新记录' + keep_en(db_table)


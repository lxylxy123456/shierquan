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

class AvatarAccount(models.Model):
	'''
		头像路径：media/images/avatar/{{ src }}-{{ sname }}.png
		注意：需要手动创建上述的文件夹
	'''
	name = models.CharField(u'文件名', default='', max_length=40)
	temp_name = models.CharField(u'原始文件名', default='', max_length=50)
	account_id = models.IntegerField(u'账户', default=0)
	relation = models.CharField(u'关系类型', default='', max_length=20)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	
	allowed_keys = ('id', 'account_id', 'relation')
	
	def __str__(self):
		return str(self.account) + str(self.image)
	class Meta:
		db_table = 'AvatarAccount'
		verbose_name = verbose_name_plural = '头像信息' + keep_en(db_table)

class AvatarTemp(models.Model):
	'''
		暂时搁置：relation
		'club'	:	社团头像
		'user'	:	用户头像
	'''
	image = models.ImageField(upload_to='images/temp/', 
			default = 'images/temp/no-img.png')
	raw_name = models.CharField(u'原始文件名', default='', max_length=40)
	account_id = models.IntegerField(u'账户', default=0)
	relation = models.CharField(u'关系类型', default='', max_length=20)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	
	allowed_keys = ()
	
	def __str__(self):
		return str(self.account) + str(self.image)
	class Meta:
		db_table = 'AvatarTemp'
		verbose_name = verbose_name_plural = '临时头像储存' + keep_en(db_table)


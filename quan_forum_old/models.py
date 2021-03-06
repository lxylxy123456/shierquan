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

class ForumGroupOld(models.Model) :
	'板块'
	status = models.IntegerField(u'是否被删除', default=0)
	account_id = models.IntegerField(u'拥有者ID', default=0)
	relation = models.CharField(u'拥有者关系', default='', max_length=600)
	simp_name = models.CharField(u'板块sname', default='', max_length=600)
	subject = models.CharField(u'板块', default='', max_length=1200)
	content = models.CharField(u'板块介绍', default='', max_length=60000)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	secret = models.BooleanField(u'是否秘密', default=False)
	topic = models.CharField(u'板块组名称', default='', max_length=60000)
		# 中文，和相同的重复

	allowed_keys = ()

	class Meta:
		db_table = 'ForumGroup-old'
		verbose_name = verbose_name_plural = '板块-旧' + keep_en(db_table)

class ForumThreadOld(models.Model) :
	'帖子'
	status = models.IntegerField(u'是否被删除', default=0)
	send_id = models.IntegerField(u'发送者ID', default=0)
	send_relation = models.CharField(u'发送者关系', default='', max_length=600)
	subject = models.CharField(u'标题', default='', max_length=1200)
	content = models.CharField(u'内容', default='', max_length=600000)
	time_update = models.DateTimeField(u'最后修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
#	account_id = models.IntegerField(u'账户ID', default=0)
#	relation = models.CharField(u'关系类型', default='', max_length=200)
	group_id = models.IntegerField(u'板块ID', default=0)
	attach_uuid = models.CharField(u'文件组标识', default='', max_length=40)
	response_number = models.IntegerField(u'回复数量', default=0)

	allowed_keys = ()

	class Meta:
		db_table = 'ForumThread-old'
		verbose_name = verbose_name_plural = '帖子-旧' + keep_en(db_table)

class ForumResponseOld(models.Model) :
	'回复'
	status = models.IntegerField(u'是否被删除', default=0)
	send_id = models.IntegerField(u'发送者ID', default=0)
	send_relation = models.CharField(u'发送者关系', default='', max_length=600)
	reply_id = models.IntegerField(u'被回复帖子ID', default=0)
	reply_relation = models.CharField(u'被回复帖子关系', default='', max_length=600)
	content = models.CharField(u'内容', default='', max_length=600000)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	thread_id = models.IntegerField(u'主题ID', default=0)
	attach_uuid = models.CharField(u'文件组标识', default='', max_length=40)

	allowed_keys = ()

	class Meta:
		db_table = 'ForumResponse-old'
		verbose_name = verbose_name_plural = '回帖-旧' + keep_en(db_table)

class ForumHistoryOld(models.Model) :
	relation = models.CharField(u'对象关系', default='', max_length=100)
	account_id = models.IntegerField(u'对象ID', default=0)
	subject = models.CharField(u'标题', default='', max_length=1200)
	content = models.CharField(u'内容', default='', max_length=600000)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)

	allowed_keys = ()

	class Meta:
		db_table = 'ForumHistory-old'
		verbose_name = verbose_name_plural = '历史-旧' + keep_en(db_table)


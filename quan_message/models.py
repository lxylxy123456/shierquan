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

class GlobalMessage(models.Model) :
	'''
		status说明:
			0:	正常
			1:	被删除

		消息关联关系		major	minor	触发动作
			#社团
				event	account	event	{ new(g), follow(g), nice(g), cancel(g)}
				signup	account	event	{ new(g), success(p+g), fail(p) }
				member	user	club	{ new(g)(通过), delete(p), core(g), 
										vice(g), normal(p), apply(g)(申请)}
				share	account	share	{ new(g), hot(g), knowledge(g), }
				club	user	club	{ new(g), update(g), follow(p+g)}
				badge	account	badge	{ new(g), grant(p+g), }
				empty	club	union	{ new(g), granted(g), fine(g), }
			#用户
				user	user	user	{ new(g), follow(g), avatar(g)}
			#	user	user	signature	{ update(g)}	#minor_id = user.id
			#	user	user	nickname	{ edit(g) }		#minor_id = user.id
				news	account	news	{ new(g), }	,
		平台
			['Windows Phone', 'Android', 'iPhone', 'iPad', 'Mobile'], 否则 'Web'
	'''
	relation = models.CharField(u'消息关联关系', default='', max_length=20)
	action = models.CharField(u'触发动作', default='', max_length=100)
	major_id = models.IntegerField(u'主关联ID', default=0)
	major_relation = models.CharField(u'主关联关系', default='', max_length=20)
	minor_id = models.IntegerField(u'副关联ID', default=0)
	minor_relation = models.CharField(u'副关联关系', default='', max_length=20, blank=True)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	platform = models.CharField(u'平台', default='', max_length=20)
	data = models.CharField(u'附加数据', default='', max_length=600, blank=True)
	status = models.IntegerField(u'是否被删除', default=0)
	
	allowed_keys = ()
	
	class Meta:
		db_table = 'GlobalMessage'
		verbose_name = verbose_name_plural = '公共消息' + keep_en(db_table)

class PrivateMessage(models.Model) :
	'''
		deleted说明:
			0:	正常
			1:	被删除
		status表示已读情况
		reference是链接
		send 和 recv 是用户或社团
		conn_relation 指明渲染使用模版
			conn_src	conn_id	说明
			event		evid	活动
			share		sid	分享
			contact		-	加好友
			hi			-	加好友（有内容）
			leave		cid	社团留言
		如果 conn_relation 不是'none'，则 conn_id 指明渲染的信息来源
	'''
#	subject = models.CharField(u'标题', default='', max_length=100)
	content = models.CharField(u'内容', default='', max_length=800)
	conn_id = models.IntegerField(u'消息关联ID', default=0)
	conn_relation = models.CharField(u'消息关联关系', default='', max_length=20)
	recv_id = models.IntegerField(u'收信者', default=0)
	recv_relation = models.CharField(u'收信关系', max_length=20)
	send_id = models.IntegerField(u'发信者', default=0)
	send_relation = models.CharField(u'发信关系', default='', max_length=20)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	reference = models.CharField(u'链接', default='', max_length=1000)
	status = models.CharField(u'状态', default='', max_length=20)
	data = models.CharField(u'数据', default='', max_length=60)
	deleted = models.IntegerField(u'是否被删除', default=0)
	
	allowed_keys = ()
	
	def __str__(self):
		return self.status + ' user: ' + str(self.recv_id) + ' conn_id: ' + str(self.conn_id)
	class Meta:
		db_table = 'PrivateMessage'
		verbose_name = verbose_name_plural = '私人消息' + keep_en(db_table)


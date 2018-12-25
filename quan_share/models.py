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

class ShareInfo(models.Model) :
	'''
		社联的sname为:club-union
		relation说明:
			club: 	社团
			user: 	个人
		category说明：#如果有增加share-record-%%s，在quan_auth.views查找并进行增加
			record-granted		材料已通过审核
			record-denied		材料未通过审核
			record-droped		材料不足
			record-broken		材料损坏
			record-waiting		等待审核（废弃，转换为 event ）
			news				[废弃]分享/新闻
			handout				分享/资料
			knowledge			分享/知识
			event				某次活动后上传的图片
			form				申请表
		status说明:
			0:	正常
			1:	被删除
	'''
	status = models.IntegerField(u'是否被删除', default=0)
	subject = models.CharField(u'标题', max_length=80, default='')
	content = models.CharField(u'内容', max_length=4000, default='')
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	account_id = models.IntegerField(u'发布者', default=0)
	relation = models.CharField(u'关系', max_length=40, default='')
	attach_uuid = models.CharField(u'文件组标识', max_length=40, default='', unique=True)
	category = models.CharField(u'类型', max_length=20, default='', blank=True)
	password = models.CharField(u'密码', max_length=40, default='', blank=True)
	visitors = models.IntegerField(u'访问次数', default=0)
	
	allowed_keys = ('id', 'subject', 'content', 'category', 'attach_uuid', 
					'visitors')
	
	def __str__(self):
		return self.subject
	class Meta:
		db_table = 'ShareInfo'
		verbose_name = verbose_name_plural = '分享' + keep_en(db_table)

class ShareInfoForm(ModelForm):
	class Meta:
		model = ShareInfo
	#	fields = ['subject']
		fields = []

class ShareAttach(models.Model) :
	'''
		category
			image		图片
			file		文件
			archive		压缩档案
		video_status
			0	视频
			1	(默认)
			2+	错误
		Video path
			/media/stream/{{ name_new }}.png
			/media/stream/{{ name_new }}.mp4
			/media/stream/{{ name_new }}.webm
	'''
	shared = models.IntegerField(u'是否被分享', default=0)
	attach_uuid = models.CharField(u'文件组标识', max_length=40)
	second_uuid = models.CharField(u'时间标识', max_length=40)
	category = models.CharField(u'文件组类型', max_length=20, blank=True)
	name_new = models.CharField(u'存储文件名', max_length=255)
	name_raw = models.CharField(u'原始文件名', max_length=255)
	description = models.CharField(u'文件描述', default='', max_length=1000, 
									blank=True)
	account_id = models.IntegerField(u'发布者', default=0)
	relation = models.CharField(u'关系', max_length=40)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	downloads = models.IntegerField(u'下载次数', default=0)
	size = models.IntegerField(u'大小', default=0)
	# 视频参数
	video_status = models.IntegerField(u'视频状态', default=1)
	video_height = models.IntegerField(u'视频高度', default=768)
	video_width = models.IntegerField(u'视频宽度', default=1366)
	mp4_status = models.IntegerField(u'mp4格式状态', default=0)
	webm_status = models.IntegerField(u'webm格式状态', default=0)
	
	allowed_keys = ('id', 'attach_uuid', 'name_raw', 'size', 'downloads')
	
	def __str__(self):
		return self.attach_uuid
	class Meta:
		db_table = 'ShareAttach'
		verbose_name = verbose_name_plural = '分享附件' + keep_en(db_table)


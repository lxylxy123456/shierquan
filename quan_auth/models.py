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

class AuthInfo(models.Model):
	'社团联合会记录'
	'''
		relation说明：
			recommendation		社团推荐（account_id为社团ID）
			amercement			坏行为记录（记录社团的）
			amercement-history	坏行为记录（已删除）
			read-notice			告知已读（account_id为用户ID，通过时间判断通知版本）
			===
			performance			星级评价审核（extra为影响力表单项）
			performance-history	已经过去的星级评价审核
				data: 状态
					preparing	正在填写
					waiting		等待审核
					denied		材料未通过审核
					droped		材料不足
					broken		材料损坏
					granted		审核通过
				extra: 影响力栏目
				score: 社联等方面的评分， json 储存
				stars: 社长申报的星级
			===
			performance-rubric	星级评价评分标准，理论上每学期只有一个
				data: 联盟简称
				extra: json 格式的数据
				account_id: 最后更改人的ID
			===
			funds				资金申请
			funds-history		已经过去的资金申请
				data :
					preparing	正在填写（可选）
					deleted		被社长删除（可选）
					submitted	已提交
					head-wait	已审核待社长查看
					head-agree	已审核社长同意
					head-deny	已审核社长拒绝
					granted		申请通过
					rejected	申请失败
					droped		材料缺失
				stars: 申请 ID
				extra: 表单项
	'''
	account_id = models.IntegerField(u'账户ID', default=0)
	relation = models.CharField(u'关系类型', default='', max_length=100)
	data = models.CharField(u'数据', default='', max_length=400, blank=True)
	extra = models.CharField(u'额外数据', default='', max_length=12000, blank=True)
	score = models.CharField(u'评分数据', default='', max_length=12000, blank=True)
	stars = models.IntegerField(u'星级数量', default=0)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)

	allowed_keys = ('id', 'account_id', 'relation', 'data', 'extra', 'score', 
					'stars')

	def __str__(self):
		return str(self.account_id) + ': ' + self.relation
	class Meta :
		db_table = 'AuthInfo'
		verbose_name = verbose_name_plural = '社联数据' + keep_en(db_table)


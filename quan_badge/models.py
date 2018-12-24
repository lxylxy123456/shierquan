from common import *

class BadgeInfo(models.Model) :
	'''
		status 说明：
			0: 正常
			1: 删除
	'''
	name = models.CharField(u'徽章标题', max_length=20)
	desc = models.CharField(u'描述', max_length=40)
	rank = models.CharField(u'等级', max_length=20)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	account_id = models.IntegerField(u'发布者', default=0)#社团
	relation = models.CharField(u'关系类型', default='', max_length=20)
	category = models.CharField(u'徽章类型', max_length=20, blank=True)
	status = models.IntegerField(u'是否被删除', default=0)
	
	allowed_keys = ('id', 'name', 'desc', 'rank', 'account_id', 'relation')
	
	def __str__(self):
		return self.name
	class Meta:
		db_table = 'BadgeInfo'
		verbose_name = verbose_name_plural = '徽章' + keep_en(db_table)

class BadgeInfoForm(ModelForm):
	class Meta:
		model = BadgeInfo
		fields = ['name', 'desc', 'rank']

class BadgeRelation(models.Model) :
	'''
		status 说明：
			0: 正常
			1: 删除
	'''
	badge_id = models.IntegerField(u'徽章ID', default=0)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	reason = models.CharField(u'授予缘由', default='', max_length=600)
	send_id = models.IntegerField(u'发送者', default=0)
	recv_id = models.IntegerField(u'接收者', default=0)
	send_relation = models.CharField(u'发送关系类型', default='', max_length=20)
	recv_relation = models.CharField(u'接收关系类型', default='', max_length=20)
	data = models.CharField(u'数据', max_length=400, blank=True)
	status = models.IntegerField(u'是否被删除', default=0)
	
	allowed_keys = ('id', 'badge_id', 'reason')
	
	def __str__(self):
		return str(self.recv_id)
	class Meta:
		db_table = 'BadgeRelation'
		verbose_name = verbose_name_plural = '徽章授予' + keep_en(db_table)

class TagInfo(models.Model) :
	subject = models.CharField(u'标签名称', max_length=200)
	content = models.CharField(u'标签描述', max_length=400)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	account_id = models.IntegerField(u'发布者', default=0)
	relation = models.CharField(u'关系类型', default='', max_length=20)
	
	allowed_keys = ()
	
	def __str__(self):
		return self.subject
	class Meta:
		db_table = 'TagInfo'
		verbose_name = verbose_name_plural = '标签' + keep_en(db_table)


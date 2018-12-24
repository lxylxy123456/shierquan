from common import *

class EmailInfo(models.Model) :
	'''
		记录所有已经发送的邮件
		status	如果出错的出错信息
		subtype in ('plain', 'html')
		charset = 'utf-8'
		category
			('password-reset', 'password-reset-used')
				account_id, category -> 相关人员
				data -> 验证代码
				relation = 'user'
	'''
	subject = models.CharField(u'标题', max_length=600, default='')
	content = models.CharField(u'内容', max_length=12000, default='')
	reciever = models.CharField(u'收件人', max_length=600, default='')
	sender = models.CharField(u'发件人', max_length=600, default='', blank=True)
	subtype = models.CharField(u'内容类型', max_length=20, default='')
	charset = models.CharField(u'字符编码', max_length=20, default='')
	# 以上是邮件本身的内容
	status = models.CharField(u'邮件发送状态', max_length=200, default='', blank=True)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	# 以下记录邮件的相关信息
	category = models.CharField(u'类型', max_length=20, default='')
	data = models.CharField(u'数据', max_length=200, default='')
	account_id = models.IntegerField(u'账户ID', default=0)
	relation = models.CharField(u'关系类型', default='', max_length=20)
	
	allowed_keys = ()
	
	def __str__(self):
		return self.subject + ' has id ' +str(self.id)
	class Meta:
		db_table = 'EmailInfo'
		verbose_name = verbose_name_plural = '邮件记录' + keep_en(db_table)


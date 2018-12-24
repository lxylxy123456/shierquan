from common import *

class NewsInfo(models.Model) :
	'''
		status说明：
			0: 正常
			1: 删除
		使用id进行索引
		"我看为了news牺牲share太多了"
			——cited from mail from mabu
	'''
	subject = models.CharField(u'标题', max_length=80, default='')
	content = models.CharField(u'内容', max_length=10000, default='')
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	account_id = models.IntegerField(u'发布者', default=0)
	relation = models.CharField(u'关系', max_length=40, default='')
	attach_uuid = models.CharField(u'文件组标识', max_length=40, default='', blank=True)
	category = models.CharField(u'类型', max_length=20, default='', blank=True)
	status = models.IntegerField(u'新闻状态', default=0)
	visited = models.IntegerField(u'阅读数量', default=0)
	
	allowed_keys = ('id', 'subject', 'content', 'attach_uuid', 'category', 
					'visited')
	
	def __str__(self):
		return self.subject
	class Meta:
		db_table = 'NewsInfo'
		verbose_name = verbose_name_plural = '新闻' + keep_en(db_table)


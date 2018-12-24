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


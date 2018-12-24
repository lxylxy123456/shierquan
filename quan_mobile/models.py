from common import *

class MobileHost(models.Model):
	account_id = models.IntegerField(u'用户ID', default=0)
	host_id = models.CharField(u'机主ID', default='', max_length=100, unique=True)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	
	allowed_keys = ()

	class Meta:
		db_table = 'MobileHost'
		verbose_name = verbose_name_plural = '移动端' + keep_en(db_table)


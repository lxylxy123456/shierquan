from common import *

class UserAgentInfo(models.Model):
	'请求UserAgent信息表'
	simp_name = models.CharField('用户', max_length=100)
	method = models.CharField('请求方法', max_length=10)
	path = models.CharField('访问路径', max_length=100)
	agent = models.CharField('User Agent', max_length=100)
	ipaddr = models.GenericIPAddressField('IP地址', null=True, protocol='both', 
											unpack_ipv4=True)
	time_create = models.DateTimeField('创建时间', auto_now_add=True)
	host = models.CharField('访问域名', max_length=30, default='')
	status_code = models.IntegerField('返回状态码', default=0)
	
	allowed_keys = ()
	
	def __str__(self):
		return ' '.join(map(repr, 
							(self.ipaddr, self.method, self.path, self.agent)
						))
	class Meta:
		db_table = 'UserAgentInfo'
		verbose_name = verbose_name_plural = '访问日志' + keep_en(db_table)

class UnwelcomeGuest(models.Model):
	'IP黑名单'
	agent = models.CharField('用户代理', max_length=100)
	ipaddr = models.GenericIPAddressField('IP地址', null=True, protocol='both', unpack_ipv4=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	
	allowed_keys = ()
	
	def __str__(self):
		return self.ipaddr + self.agent
	class Meta:
		db_table = 'UnwelcomeGuest'
		verbose_name = verbose_name_plural = '黑名单' + keep_en(db_table)

class RealNameInfo(models.Model):
	'真实姓名认证'
	name = models.CharField(u'姓名', default='', max_length=400)
	status = models.CharField(u'身份', default='', max_length=60)
	used = models.IntegerField(u'注册情况', default=0)
	account_id = models.IntegerField(u'账户ID', default=0)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	
	allowed_keys = ()
	
	def __str__(self):
		return self.name + ' status ' + self.status + ' used ' + str(self.used)
	class Meta:
		db_table = 'RealNameInfo'
		verbose_name = verbose_name_plural = '真实姓名记录' + keep_en(db_table)

class LoginRecord(models.Model) :
	'登录记录'
	username = models.CharField(u'用户名', default='', max_length=30)
	password = models.CharField(u'密码', default='', max_length=128)
	agent = models.CharField('User Agent', max_length=100)
	time = models.DateTimeField(u'创建时间', auto_now_add=True)
	
	allowed_keys = ()
	
	def __str__(self):
		return self.username + self.password
	class Meta :
		db_table = 'LoginRecord'
		verbose_name = verbose_name_plural = '登录记录' + keep_en(db_table)


from common import *

# 编写者已被Django的ManyToMany 'self'整疯

class UserAccount(models.Model):
	basic = models.OneToOneField(User, unique=True)
	grade = models.IntegerField(u'年级', default=0)
	phone = models.CharField(u'电话', default='', max_length=12)
	nickname = models.CharField(u'用户昵称', default='', max_length=100, blank=True)
	signature = models.CharField(u'签名', default='', max_length=200, blank=True)
	status = models.CharField(u'用户身份', default='', max_length=40, blank=True)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	pinyin = models.CharField(u'全名拼音', default='', max_length=360, blank=True)
	visitors = models.IntegerField(u'访问次数', default=0)
	
	allowed_keys = ('id', 'grade', 'nickname', 'signature', 'visitors')

	# Reference: https://docs.djangoproject.com/en/1.7/ref/models/instances/ 
	def __str__(self):
		return self.basic.email
	class Meta:
		db_table = 'UserAccount'
		verbose_name = verbose_name_plural = '用户扩展' + keep_en(db_table)

class UserForm(ModelForm):
	class Meta:
		# first_name:	真实姓名
		# last_name:	昵称
		model = User
		fields = ['first_name', 'last_name', 'username', 'password', 'email']

class UserAccountForm(ModelForm):
	class Meta:
		model = UserAccount
		fields = ['grade', 'phone']

class ClubAccount(models.Model):
	'''
		category: 社团联盟的英文名称
	'''
	full_name = models.CharField(u'社团全称', default='', max_length=60)
	simp_name = models.CharField(u'社团简称', default='', max_length=30)
	category = models.CharField(u'社团类型', default='', max_length=30)
	simp_intro = models.CharField(u'社团简短介绍', default='', max_length=360)
	full_intro = models.CharField(u'社团详细说明', default='', max_length=12000)
	rank = models.IntegerField(u'QuanRank', default=0)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	pinyin = models.CharField(u'社团全称拼音', default='', max_length=360)
	visitors = models.IntegerField(u'访问次数', default=0)
	
	allowed_keys = ('id', 'full_name', 'simp_name', 'simp_intro', 'full_intro', 
					'visitors')
	
	def __str__(self):
		return self.full_name
	class Meta:
		db_table = 'ClubAccount'
		verbose_name = verbose_name_plural = '社团' + keep_en(db_table)

class ClubAccountForm(ModelForm):
	class Meta:
		model = ClubAccount
		fields = ['simp_name', 'full_name', 'simp_intro', 'full_intro', 'category']

class ClubAlias(models.Model) :
	'定义社团别名'
	status = models.IntegerField(u'是否被删除', default=0)
	club_id = models.IntegerField(u'社团ID', default=0)
	alias = models.CharField(u'别名', default='', max_length=30)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	
	allowed_keys = ('id', 'club_id', 'alias')
	
	def __str__(self):
		return 'club %d has alias "%s"' % (self.club_id, self.alias)
	class Meta:
		db_table = 'ClubAlias'
		verbose_name = verbose_name_plural = '社团别名' + keep_en(db_table)

class AccountRelation(models.Model) :
	'定义用户/社团与用户/社团的关系'
	'''
		relation说明：
			head				用户A是社团B的社长
			vice				用户A是社团B的副社长
			core				用户A是社团B的核心(和member共存，默认社长、副社长为核心)
			member				用户A是社团B的社员
			member-break		用户A是社团B的历史社员
			member-wait			用户A是社团B的待审核社员
			member-wait-deny	用户A申请社团B被拒绝
			follower			用户A关注社团B
			uu-follower			用户A关注用户B
			uu-follower-break	取消用户A关注用户B
			cc-friend			社团A和社团B为友好社团
			uu-friend			用户好友			（最开始A提出请求）
			uu-friend-wait		等待用户好友		（A提出请求）
			uu-friend-break		断开的用户好友关系	（最开始A提出请求）
			uu-friend-deny		拒绝申请			（最开始A提出请求）
			qrank				月份A时社团B的QuanRank
	'''
	account_id_A = models.IntegerField(u'账户ID-A', default=0)
	account_id_B = models.IntegerField(u'账户ID-B', default=0)
	relation = models.CharField(u'关系类型', default='', max_length=200)
	data = models.CharField(u'数据', null=True, max_length=200, blank=True)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	
	allowed_keys = ('id', 'account_id_A', 'account_id_B', 'relation')
	
	def __str__(self):
		return str(self.account_id_A) + 'is the' + self.relation + 'of' + str(self.account_id_B)
	class Meta:
		db_table = 'AccountRelation'
		verbose_name = verbose_name_plural = '账户关系' + keep_en(db_table)


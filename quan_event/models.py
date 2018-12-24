from common import *

class EventInfo(models.Model) :
	'''
		relation说明：
			user	发起事件者为用户
			club	发起事件者为社团
		category :
			history			历史活动
			''				正常活动
			history-deleted	被删除历史活动
			deleted			被删除正常活动
	'''
	subject = models.CharField(u'活动标题', max_length=60)
	content = models.CharField(u'活动内容', max_length=600)
	time_set = models.DateTimeField(u'开始时间')
	time_end = models.DateTimeField(u'结束时间')
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	location = models.CharField(u'活动地点', max_length=60)
	category = models.CharField(u'活动类型', max_length=20, blank=True)
	account_id = models.IntegerField(u'账户ID', default=0)
	relation = models.CharField(u'关系类型', default='', max_length=20)
	status = models.CharField(u'活动状态', default='on', max_length=20)
	visitors = models.IntegerField(u'访问次数', default=0)
	
	allowed_keys = ('id', 'subject', 'content', 'time_set', 'time_end', 
					'location', 'visitors')
	
	def __str__(self):
		return self.subject + ' has id ' +str(self.id)
	class Meta:
		db_table = 'EventInfo'
		verbose_name = verbose_name_plural = '活动' + keep_en(db_table)

class EventInfoForm(ModelForm):
	class Meta:
		model = EventInfo
		fields = ['subject', 'location']

class EventQuest(models.Model) :
	event_id = models.IntegerField(u'活动ID', default=0)
	answer = models.CharField(u'答案', max_length=20)
	quest = models.CharField(u'问题', max_length=80)
	option_A = models.CharField(u'选项A', max_length=80)
	option_B = models.CharField(u'选项B', max_length=80)
	option_C = models.CharField(u'选项C', max_length=80)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	token = models.IntegerField(u'二维码验证', default=0)
	status = models.CharField(u'状态', max_length=40)
	
	allowed_keys = ('quest', 'option_A', 'option_B', 'option_C')
	
	def __str__(self):
		return str(self.event_id) + self.quest
	class Meta:
		db_table = 'EventQuest'
		verbose_name = verbose_name_plural = '活动签到' + keep_en(db_table)

class EventQuestForm(ModelForm):
	class Meta:
		model = EventQuest
		fields = ['quest', 'option_A', 'option_B', 'option_C', 
					'answer']

class EventRelation(models.Model) :
	'''
		relation说明：
			nice			手气不错（赞）
			follower		关注者
			signup			签到

		status：
			failure			签到失败
			success			签到成功
	'''
	account_id = models.IntegerField(u'账户ID', default=0)
	relation = models.CharField(u'关系类型', default='', max_length=20)
	event_id = models.IntegerField(u'事件ID', default=0)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	status = models.CharField(u'状态', max_length=20, blank=True)
	
	allowed_keys = ()
	
	def __str__(self):
		return str(self.account_id) +' is '+self.relation+' of '+ str(self.event_id)
	class Meta:
		db_table = 'EventRelation'
		verbose_name = verbose_name_plural = '活动关系' + keep_en(db_table)

class ShareEventRelation(models.Model) :
	'''
		记录 Share 和 Event 的关联
		status: 
			0	正常
			1	删除
	'''
	share_id = models.IntegerField(u'分享ID', default=0)
	event_id = models.IntegerField(u'事件ID', default=0)
	time_create = models.DateTimeField(u'创建时间', auto_now_add=True)
	time_update = models.DateTimeField(u'修改时间', auto_now=True)
	status = models.IntegerField(u'是否被删除', default=0)
	
	allowed_keys = ()
	
	def __str__(self):
		if self.status :
			return 'share %d --  -- event %d' % (self.share_id, self.event_id)
		else :
			return 'share %d --==-- event %d' % (self.share_id, self.event_id)
	class Meta:
		db_table = 'ShareEventRelation'
		verbose_name = verbose_name_plural = '分享活动关联' + keep_en(db_table)


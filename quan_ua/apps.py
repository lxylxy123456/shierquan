from django.apps import AppConfig
from django.conf import settings

class NameConfig(AppConfig) :
	name = 'quan_ua'
	verbose_name = '用户统计' + (settings.KEEP_EN and ' (%s)' % name)


from django.apps import AppConfig
from django.conf import settings

class NameConfig(AppConfig) :
	name = 'quan_event'
	verbose_name = '活动' + (settings.KEEP_EN and ' (%s)' % name)


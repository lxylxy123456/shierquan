from django.apps import AppConfig
from django.conf import settings

class NameConfig(AppConfig) :
	name = 'quan_message'
	verbose_name = '消息' + (settings.KEEP_EN and ' (%s)' % name)


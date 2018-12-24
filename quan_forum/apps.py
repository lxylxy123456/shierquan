from django.apps import AppConfig
from django.conf import settings

class NameConfig(AppConfig) :
	name = 'quan_forum'
	verbose_name = '论坛' + (settings.KEEP_EN and ' (%s)' % name)


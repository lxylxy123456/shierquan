from django.apps import AppConfig
from django.conf import settings

class NameConfig(AppConfig) :
	name = 'quan_mobile'
	verbose_name = '客户端' + (settings.KEEP_EN and ' (%s)' % name)


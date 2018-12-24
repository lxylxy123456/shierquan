from django.apps import AppConfig
from django.conf import settings

class NameConfig(AppConfig) :
	name = 'quan_square'
	verbose_name = '广场' + (settings.KEEP_EN and ' (%s)' % name)


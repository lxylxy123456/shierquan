from django.apps import AppConfig
from django.conf import settings

class NameConfig(AppConfig) :
	name = 'quan_center'
	verbose_name = '主页' + (settings.KEEP_EN and ' (%s)' % name)


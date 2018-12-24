from django.apps import AppConfig
from django.conf import settings

class NameConfig(AppConfig) :
	name = 'quan_share'
	verbose_name = '分享' + (settings.KEEP_EN and ' (%s)' % name)


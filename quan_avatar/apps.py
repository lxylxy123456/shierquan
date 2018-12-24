from django.apps import AppConfig
from django.conf import settings

class NameConfig(AppConfig) :
	name = 'quan_avatar'
	verbose_name = '头像' + (settings.KEEP_EN and ' (%s)' % name)


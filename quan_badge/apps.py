from django.apps import AppConfig
from django.conf import settings

class NameConfig(AppConfig) :
	name = 'quan_badge'
	verbose_name = '徽章' + (settings.KEEP_EN and ' (%s)' % name)


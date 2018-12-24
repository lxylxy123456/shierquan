from django.apps import AppConfig
from django.conf import settings

class NameConfig(AppConfig) :
	name = 'quan_account'
	verbose_name = '账户' + (settings.KEEP_EN and ' (%s)' % name)


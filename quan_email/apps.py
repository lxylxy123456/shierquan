from django.apps import AppConfig
from django.conf import settings

class NameConfig(AppConfig) :
	name = 'quan_email'
	verbose_name = '邮件' + (settings.KEEP_EN and ' (%s)' % name)


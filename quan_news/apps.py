from django.apps import AppConfig
from django.conf import settings

class NameConfig(AppConfig) :
	name = 'quan_news'
	verbose_name = '新闻' + (settings.KEEP_EN and ' (%s)' % name)


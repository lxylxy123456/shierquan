# 
# Shierquan - a website similar to shiyiquan.net; see README.md
# Copyright (C) 2018  lxylxy123456
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# 

"""
Django settings for shierquan project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%+g&ol14=qffr&9mdshwy-@r^)-cg6%s7g@h6zqrr8lrz=$_iu'

import socket, re

hostname = socket.gethostname()

if 'SERVER' not in hostname :
	hostname = 'laptop'

if hostname in ('laptop', ) :
    DEBUG = True
    ALLOWED_HOSTS = [
        '*', 
    ]
else:
	# SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False
    ALLOWED_HOSTS = [
       '.shierquan.tk',	# Allow domain and subdomains
       '.shierquan.tk.',	# Also allow FQDN and subdomains
    ]

KEEP_EN = 'yes'	# 这里的值只要是真就会被忽略。如果不想保留英文，将其改为 ''


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'quan_account.apps.NameConfig',
    'quan_avatar.apps.NameConfig',
    'quan_auth.apps.NameConfig',
    'quan_badge.apps.NameConfig',
    'quan_center.apps.NameConfig',
    'quan_event.apps.NameConfig',
    'quan_email.apps.NameConfig',
    'quan_forum.apps.NameConfig',
    'quan_forum_old.apps.NameConfig',
    'quan_message.apps.NameConfig',
    'quan_share.apps.NameConfig',
    'quan_square.apps.NameConfig',
    'quan_ua.apps.NameConfig',
    'quan_news.apps.NameConfig', 
    'quan_mobile.apps.NameConfig', 
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware', 	# added 20170302
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
#    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'shierquan.urls'

WSGI_APPLICATION = 'shierquan.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if hostname in () :
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
		}
	}
else :
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'shierquan',
			'USER': 'postgres',
			'PASSWORD': open(os.path.join(os.path.dirname(__file__), 
											'db_passwd.txt')).read(),
			'HOST': '127.0.0.1',
			'PORT': '5432',
		}
	}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + STATIC_URL
STATIC_DICT = {
    'quan_event': BASE_DIR + '/quan_event/static',
    'quan_share': BASE_DIR + '/quan_share/static',
    'quan_square': BASE_DIR + '/quan_square/static',
    'quan_news': BASE_DIR + '/quan_news/static',
    'quan_ua': BASE_DIR + '/quan_ua/static',
}

MEDIA_URL = '/media/'
MEDIA_DICT = {
    'document_root': BASE_DIR + MEDIA_URL,
}
if hostname in ('laptop', ):
	MEDIA_ROOT = BASE_DIR + MEDIA_URL
else :
	MEDIA_ROOT = '/opt/shierquan' + MEDIA_URL

ADMINS = (
    ('Admin', 'admin@shierquan.tk'),
    ('Logger', 'shierquan@localhost'),
)

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'quan-logger': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

if hostname in ('HCCSERVER', ) :
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else :
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SERVER_EMAIL = 'admin@shierquan.tk'

from django.conf import global_settings
handle_mod = 'shierquan.handler.UploadProgressCachedHandler'
FILE_UPLOAD_HANDLERS = [handle_mod, ] + \
    list(global_settings.FILE_UPLOAD_HANDLERS)

if hostname in ('HCCSERVER', 'laptop', ) :
	CACHES = {
		'default': {
			'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
			'LOCATION': '127.0.0.1:11211',
		}
	}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG, 
            'context_processors': [
                 'django.contrib.auth.context_processors.auth',
            ]
        },
    },
]


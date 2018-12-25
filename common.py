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

'''
	这个 Python 脚本收录了经常引用的 Django 和 Python 模块，来防止文件开头引用过多过乱
'''

# For models.py
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
keep_en = lambda x: settings.KEEP_EN and ' (%s)' % x

# For views.py

# Python modules
from datetime import datetime, timedelta
from hashlib import md5
from html.parser import HTMLParser
from PIL import Image
from urllib import parse
from zipfile import ZipFile
import base64, collections, ipaddress, itertools, json, logging, mimetypes
import os, pypinyin, qrcode, random, re, socket, sys, threading, time
import traceback, uuid

# logger
logger = logging.getLogger('quan-logger')

# Shierquan modules
from translate import get_language, translate as t_

# Django modules
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sitemaps import Sitemap
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.exceptions import PermissionDenied as Http403
from django.core.files import File
from django.core.files.uploadhandler import FileUploadHandler
from django.db.models import Q
from django.db.utils import DataError
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect as Http302
from django.http import HttpResponse, StreamingHttpResponse, Http404
from django.middleware.csrf import get_token
from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf
from django.template.loader import get_template
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


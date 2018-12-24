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

# Shiyiquan modules
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


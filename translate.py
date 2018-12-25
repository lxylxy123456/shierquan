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

import os, pickle, socket
from django.utils import translation
from django.conf import settings

load = lambda x: pickle.load(open(os.path.join(settings.BASE_DIR, x), 'rb'))
translate_cache_en = load('locale/en.pickle')
translate_cache_ja = load('locale/ja.pickle')

def get_language(request=None) :
	'检测语言， Snap 中对此函数的调用在 documentation 中应该有 [翻] 标记'
	import threading
	if request == None :
		try :
			request = settings.request_thread_safe.request
			# 灵感来自 /usr/lib64/python3.5/site-packages/django/utils/
			#			translation/trans_real.py
		except Exception :
			pass
	if request != None :
		language = {
			'en.shierquan.tk': 'en', 
			'ja.shierquan.tk': 'ja', 
			'zh.shierquan.tk': 'zh', 
		}.get(request.META.get('HTTP_HOST'))
		if language :
			return language
	if socket.gethostname() == 'HCCSERVER' :
		return 'zh'
	if 'en' in translation.get_language() :
		return 'en'
	if 'ja' in translation.get_language() :
		return 'ja'
	else :
		return 'zh'

def translate(content, request=None) :
	if get_language(request) == 'en' :
		return translate_cache_en.get(content) or content
	if get_language(request) == 'ja' :
		return translate_cache_ja.get(content) or content
	return content


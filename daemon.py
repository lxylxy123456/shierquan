#!/usr/bin/env python3

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

import os, sys, django, socket
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shierquan.settings")
django.setup()
from quan_share.views import *

if __name__ == "__main__":
	while 1 :
		try :
			time.sleep(1)
			for i in ShareAttach.objects.filter(webm_status=0, video_status=0) :
				ShareSnap.stream_process(i, 'webm')
			for i in ShareAttach.objects.filter(mp4_status=0, video_status=0) :
				ShareSnap.stream_process(i, 'mp4')
		except Exception as e :
			print(repr(e))


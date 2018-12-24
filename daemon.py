#!/usr/bin/env python3
import os, sys, django, socket
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shiyiquan.settings")
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


from .models import *

from quan_message.models import *

from quan_account.views import *
from quan_avatar.views import AvatarSnap
from quan_message.views import MessageSnap
from quan_ua.views import *

#TODO： 多张图片上传/大图片上传
class ShareSnap:
	def share_find_by_uuid(suid) :
		'attach_uuid -> ShareInfo()'
		try :
			return ShareInfo.objects.get(attach_uuid=suid, status=0)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def download_find(suid, tid, archive='') :
		'得到 (原文件名, 文件系统路径) ，用于文件下载'
		if archive :
			query = { 'attach_uuid': suid, 'category': 'archive' }
		else :
			query = { 'attach_uuid': suid, 'second_uuid': tid }
		try :
			assert ShareSnap.share_find_by_uuid(suid)
			qry = ShareAttach.objects.get(**query)
		except (ObjectDoesNotExist, MultipleObjectsReturned, AssertionError) :
			raise Http404('找不到文件')
		qry.downloads += 1
		qry.save()
		name_new = qry.name_new
		if archive :
			spath = os.path.join(settings.MEDIA_ROOT, 'archives', name_new)
		else :
			sname = AccountSnap.sname_find_by_aid(qry.relation, qry.account_id)
			spath = os.path.join(settings.MEDIA_ROOT, 'files', sname, name_new)
		return qry.name_raw, spath

	def thumbnail_find(suid, size, tid='') :
		'''
			size in ('small', 'medium', 'large', 'exlarge')
		'''
		if not ShareSnap.share_find_by_uuid(suid) :
			return None
		if size not in ('small', 'medium', 'large', 'exlarge') :
			size = 'exlarge'
		qry_root = ShareAttach.objects.filter(attach_uuid=suid)
		if tid :
			qry_root = qry_root.filter(second_uuid=tid)
		# try image
		qry = qry_root.filter(category='image')
		if qry.exists() :
			return '/media/images/share/%s/%s' % (size, qry[0].name_new)
		# try video
		qry = qry_root.filter(video_status=0)
		if qry.exists() :
			return '/media/images/share/%s/%s.png' % (size, qry[0].name_new)
		# Not found
		return None

	def system(command, limit) :
		'通过 subprocess.Popen 执行系统命令并得到返回数据 (return, stdout, stderr)'
		import subprocess
		pro = subprocess.Popen(command.split(), stdin=-1, stdout=-1, stderr=-1)
		try :
			out, err = pro.communicate(b'', 7200)
		except subprocess.TimeoutExpired :
			out, err = pro.stdout.read(), pro.stderr.read()
		return pro.returncode, out, err

	def stream_process(qry, file_type) :
		'[stream] 视频 -> mp4 / webm'
		sname = UserSnap.sname_find_by_uid(qry.account_id)
		fdir = os.path.join(settings.MEDIA_ROOT, 'files', sname, qry.name_new)
		target = os.path.join(settings.MEDIA_ROOT, 'stream', qry.name_new)
		if file_type == 'mp4' :
			cmd = ('ffmpeg -i %s -vcodec libx264 -profile:v baseline -level 3.0'
				' -strict -2 %s.mp4') % (fdir, target)
			ret, out, err = ShareSnap.system(cmd, 7200)
			if ret != 0 :	# 还有可能是 None ，表示在运行时因为超时被中断
				qry.mp4_status = 2
			else :
				qry.mp4_status = 1
			open(target + '.mp4.stdout', 'wb').write(out)
			open(target + '.mp4.stderr', 'wb').write(err)
		elif file_type == 'webm' :
			cmd = 'ffmpeg -i %s %s.webm' % (fdir, target)
			ret, out, err = ShareSnap.system(cmd, 7200)
			if ret != 0 :	# 还有可能是 None ，表示在运行时因为超时被中断
				qry.webm_status = 2
			else :
				qry.webm_status = 1
			open(target + '.webm.stdout', 'wb').write(out)
			open(target + '.webm.stderr', 'wb').write(err)
		qry.save()

	def add_process() :
		'[stream] fork 新的daemon.py进程'
		lock = '/tmp/shiyiquan-daemon-lock-file'
		daemon = os.path.join(settings.BASE_DIR, 'daemon.py')
		if not os.path.exists(lock) :
			logger.error('open daemon lock file 1 ' + repr(datetime.now()))
			open(lock, 'w')
			logger.error('open daemon lock file 2 ' + repr(datetime.now()))
			os.system('nohup python3 %s > %s &' % (daemon, lock))
			logger.error('open daemon lock file 3 ' + repr(datetime.now()))

	def stream_thumbnail(mod, sname=None) :
		'Processing Video, mod为ShareAttach体，应该为1，需要在函数外部save'
		if sname == None :
			sname = UserSnap.sname_find_by_uid(mod.account_id)
		fdir = os.path.join(settings.MEDIA_ROOT, 'files', sname, mod.name_new)
		directory = os.path.join(settings.MEDIA_ROOT, 'stream', mod.name_new)
		# check by filename
		if mod.video_status != 1 :
			return
		guess = mimetypes.guess_type(mod.name_raw)
		if guess and guess[0] and guess[0].split('/', 1)[0] != 'video' :
			mod.video_status = 2
			return
		# thumbnail and check
		cmd = 'ffmpeg -ss 00:00:00 -i %s -f image2 -vframes 1 -y %s.png' \
			% (fdir, directory)
		print(cmd)
		if os.system(cmd) :
			mod.video_status = 3
			return
		try :
			thumbnail = Image.open('%s.png' % directory)
			mod.video_width, mod.video_height = thumbnail.size
			mod.video_status = 0
			ShareSnap.add_process()	# process
		except OSError :
			mod.video_status = 4
			return
		try :
			ShareSnap.share_thumbnail(True, mod.name_new)
		except FileNotFoundError :
			pass

	def muti_create(files, src, aid, attach_uuid) :
		'记录附件列表，成功返回True，失败返回错误消息'
		if len(files) == 0 :
			raise Snap.error('似乎没有添加文件？')
		for f in files:
			# Max: 1.8GB
			if f.size > 1800000000:
				raise Snap.error('文件过大[已抛弃]')
		sname = AccountSnap.sname_find_by_aid(src, aid)
		for f in files:
			nsecond = '%07d' % (time.time() % 1 * 10000000)
			suffix = f.name.rsplit('.', 1)[-1]
			fname = '[%s][%s].%s' % (attach_uuid, nsecond, suffix)
			fdir = os.path.join(settings.MEDIA_ROOT, 'files', sname + '/')
			try :
				os.mkdir(fdir)
			except FileExistsError :
				pass
			try :
				output = open(fdir + fname, 'wb')
			except UnicodeEncodeError :
				t,v,tb = sys.exc_info()
#				logger.error('t ' + str(t))
#				logger.error('v ' + str(v))
			for chunk in f.chunks(): 
				output.write(chunk)
			output.close()
#			logger.error("testing...p2")
			attach_type = 'file'
			try :
				if suffix.lower() in ('tif', 'psd', 'thm') :
					raise OSError
				img = Image.open(fdir + fname)
				try :
					ShareSnap.share_thumbnail(sname, fname)
					attach_type = 'image'
				except Exception as e :
					logger.error('share1\t%s\t%s' % (str(type(e)), str(e)))
			except OSError:
				pass	# Not an image file
#				logger.error('Not an image file.')
			except Exception as e:
				t,v,tb = sys.exc_info()
#				logger.error('t ' + str(t))
#				logger.error('v ' + str(v))
#			logger.error("testing...p3")
			mod = ShareAttach(name_raw=f.name, name_new=fname, relation=src, 
					account_id=aid, attach_uuid=attach_uuid, video_status=1, 
					second_uuid=nsecond, category=attach_type)
			ShareSnap.stream_thumbnail(mod, sname)
			mod.save()
		return True

	def size_calc(qry) :
		'计算ShareAttach中的附件大小，返回总数'
		total = 0
		for i in qry :
			if i.category == 'archive' :
				spath = os.path.join \
					(settings.MEDIA_ROOT, 'archives', i.name_new)
			else :
				sname = AccountSnap.sname_find_by_aid(i.relation, i.account_id)
				spath = os.path.join \
					(settings.MEDIA_ROOT, 'files', sname, i.name_new)
			i.size = os.path.getsize(spath)
			total += i.size
			i.save()
		return total

	def url_find_by_attach(attach) :
		'得到访问的链接'
		return '/share/download/?uuid=%s&tid=%s;' % \
					(attach.attach_uuid, attach.second_uuid)

	def uuid_find_by_sid(sid) :
		qry = ShareInfo.objects.filter(status=0, id=sid)
		if qry.count() == 0 :
			return None
		else :
			return qry[0].attach_uuid

	def union_record_find() :
		'得到社联通知（用于主页显示）'
		try :
			cid = [
				ClubSnap.cid_find_by_sname('club-union'), 
				ClubSnap.cid_find_by_sname('hcc-computer-community'), 
			]
		except Http404 :
			return None
		try :
			data = ShareInfo.objects.filter(relation='club', category='event', 
					status=0, account_id__in=cid).order_by('-time_create')[0]
		except IndexError :
			return None
		return {
			'data': data, 
			'file_list': ShareSnap.file_list_find_by_suid(data.attach_uuid), 
		}

	def sid_find_by_uuid(suid) :
		'share.uuid->sid'
		try :
			return ShareInfo.objects.get(status=0, attach_uuid=suid).id
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def file_list_find_by_suid(suid, no_qry=False, no_arc=True) :
		'为/share/uuid/提供文件列表'
		qry = ShareAttach.objects.filter(attach_uuid=suid)
		attach_list = []
		for i in qry :
			if no_qry :
				data = {
					'name_raw': i.name_raw, 
					'downloads': i.downloads, 
				}
			else :	
				data = i
			if no_arc and i.category == 'archive' :
				continue
			attach_list.append({
				'data': data, 
				'url': ShareSnap.url_find_by_attach(i), 
				'name': i.name_raw, 
				'size': ChineseSnap.byte_exchange(i.size), 
			})
		return attach_list

	def image_list_find_by_suid(suid) :
		'为/share/uuid/提供图片列表'
		qry = ShareAttach.objects.filter(attach_uuid=suid, category='image')
		attach_list = []
		for i in qry :
			url = ShareSnap.url_find_by_attach(i)
			attach_list.append({
				'url': url, 
				'data': i, 
				'name': i.name_raw, 
				'thumbnail': ShareSnap.thumbnail_find \
											(suid, 'exlarge', i.second_uuid)
			})
		return attach_list

	def stream_list_find_by_suid(suid) :
		'为/share/uuid/提供视频列表'
		qry = ShareAttach.objects.filter(attach_uuid=suid, video_status=0)
		stream_list = []
		for i in qry :
			if i.webm_status == 1 and i.mp4_status == 1 :
				status = 1	# 完成
			elif i.webm_status == 2 or i.mp4_status == 2 :
				status = 2	# 错误
			else :
				status = 0	# 等待
			sname = UserSnap.sname_find_by_uid(i.account_id)
			stream_list.append({
				'data': i, 
				'url': '/media/stream/' + i.name_new, 
				'download': ShareSnap.url_find_by_attach(i), 
				'status': status, 
				'show_player': i.webm_status == 1 or i.mp4_status == 1, 
			})
		return stream_list

	def attach_find_by_uuid(attach_uuid) :
		'获取attach的qry'
		return ShareAttach.objects.filter(attach_uuid=attach_uuid)

	def share_find_by_sid(sid) :
		'获取share'
		try :
			return ShareInfo.objects.get(status=0, id=sid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def uuid_create() :
		'生成UUID'
		while True:
			attach_uuid = str(uuid.uuid1())[0:8]
			if not ShareSnap.share_find_by_uuid(attach_uuid) and \
				not ShareSnap.attach_find_by_uuid(attach_uuid).exists() :
				return attach_uuid

	def limit_check(src, aid) :
		'是否分享数量正常（一天最多10个）'
		day = datetime.now().date()
		qry = ShareInfo.objects.filter(status=0, relation=src, account_id=aid, 
				time_create__gte=datetime(day.year, day.month, day.day))
		return qry.count() <= 10

	def image_list_by_aid(src, aid) :
		'按照最新返回所有图片'
		share = ShareSnap.share_find_by_aid(src, aid)
		uuid_list = share.values_list('attach_uuid', flat=True)
		return ShareAttach.objects.filter(attach_uuid__in=uuid_list, 
								category='image').order_by('-time_create')

	def mix_find(sname) :
		'对于img_list得到图片并储存，返回url'
		directory = 'images/club-%s/mixed.png' % sname
		if os.path.exists(os.path.join(settings.MEDIA_ROOT, directory)) :
			return '/media/' + directory
		else :
			return None

	def mix_create(cid) :
		'希望在分享更新后触发，成功返回True'
		def image_generator(cid) :
			'''
				如果一个社团有很多分享，就会将其全都打开一遍
				因此这里使用了 yield 返回一个生成器，仅仅打开需要数量的文件
			'''
			for i in ShareSnap.image_list_by_aid('club', cid) :
				suid = i.attach_uuid
				tid = i.second_uuid
				try :
					yield Image.open(ShareSnap.download_find(suid, tid)[1])
				except (Http404, FileNotFoundError) :
					continue

		img4 = ShareSnap.three_square(image_generator(cid))
		if img4 == None :
			return None
		dir_common = 'images/club-%s/' % ClubSnap.sname_find_by_cid(cid)
		try :
			os.mkdir(os.path.join(settings.MEDIA_ROOT, dir_common))
		except FileExistsError :
			pass
		img4.save(os.path.join(settings.MEDIA_ROOT, dir_common, 'mixed.png'))
		return True

	def three_square(pictures) :
		'取九张图片，组成 3*3 的大图'
		h = 768 // 3
		w = 900 // 3
		sum_picture = Image.new('RGBA', (w * 3, h * 3))
		added = 0
		for i in pictures :
			pic_w, pic_h = i.size
			if pic_w < w or pic_h < h:
				continue
			#sized = i.resize((w, int(pic_h*w/pic_w)))
			#siz_w, siz_h = sized.size
			#if sized.size[1]<h:
			#	continue
			croped = i.crop(((pic_w - w) // 2, (pic_h - h) // 2, 
							(pic_w + w) // 2, (pic_h + h) // 2))
			sum_picture.paste(croped, ((added // 3) * w, (added % 3) * h, 
								(added // 3 + 1) * w, (added % 3 + 1) * h))
			added += 1
			if added == 9:
				return sum_picture
		return None		# 没有足够的图片

	def chat_find(sid) :
		'得到谈话列表（废弃可能）'
		qry = PrivateMessage.objects.filter \
				(conn_id=sid, conn_relation='share-im', 
				recv_id=sid, recv_relation='share').order_by('-time_create')
		chat_list = []
		for i in qry :
			uid = UserSnap.uid_find_by_sname(i.subject)
			chat_list.append({'data': i, 
				'avatar': AvatarSnap.avatar_find('user', uid)})
		return chat_list

	def chat_save(sid, cont, uid) :
		'储存chat的内容，返回是否成功'
		sname = UserSnap.sname_find_by_uid(uid)
		if sname == None :
			return False
		PrivateMessage(data=cont, conn_id=sid, 
			conn_relation='share-im', recv_id=sid, recv_relation='share').save()
		return True

	def chat_frequent(uid, suid) :
		'chat频率是否正常'
		sid = ShareSnap.sid_find_by_uuid(suid)
		sname = UserSnap.sname_find_by_uid(uid)
		qry = PrivateMessage.objects.filter(send_id=sid, send_relation='user', 
				conn_id=sid, conn_relation='share-im').order_by('-time_create')
		if not qry.count() :
			return True
		exc = qry[0].time_create + timedelta(0, 20)
		if datetime.now() >= exc :
			return True
		else :
			return False

	def share_frequent(src, aid) :
		'share频率是否正常'
		fsa = datetime.now() - timedelta(0, 5)	# 五秒前, Five Seconds Ago
		qry = ShareSnap.share_find_by_aid(src, aid).filter(time_create__gte=fsa)
		return not qry.exists()

	def chat_message_notify_find(sid) :
		qry = ShareInfo.objects.filter(status=0, id=sid)
		if qry.count() == 0 :
			return []
		uid_list = [qry[0].account_id]
		qry = PrivateMessage.objects.filter \
				(conn_id=sid, conn_relation='share-im', 
				recv_id=sid, recv_relation='share').order_by('-time_create')
		if qry.exists() :
			uid = UserSnap.uid_find_by_sname(qry[0].subject)
			if uid != uid_list[0] :
				uid_list.append(uid)
		return uid_list

	def share_search(query) :
		return ShareInfo.objects.filter(Q(subject__icontains=query) | 
										Q(content__icontains=query), 
										status=0, relation='club')

	def share_find_by_aid(src, aid) :
		return ShareInfo.objects.filter \
			(status=0, account_id=aid, relation=src).order_by('-time_create')

	def share_thumbnail(sname, name) :
		'''
			将
				media/files/sname/[name]
			计算为
				media/images/share/[大小]/[name]
			的文件。
			sname = True  ===>  被认为是视频，存储后缀添加 ".png"
		'''
		if sname == True :
			name += '.png'
			path = os.path.join(settings.MEDIA_ROOT, 'stream', name)
		else :
			path = os.path.join(settings.MEDIA_ROOT, 'files', sname, name)
		im = Image.open(path)
		for i in ((32, 32, 'small'), (64, 64, 'medium'), (128, 128, 'large'), 
					(300, 300, 'exlarge')) :
			path_new = os.path.join(settings.MEDIA_ROOT, 'images', 'share', 
				i[2], name)
			if os.path.exists(path_new) :
				continue
			if i[2] == 'exlarge' :
				tmp = im
				if im.size[0] < im.size[1] :
					tmp.thumbnail((i[0], im.size[1] / im.size[0] * i[0]))
				else :
					tmp.thumbnail((im.size[0] / im.size[1] * i[0], i[0]))
			else :
				if im.size[0] < im.size[1] :
					tmp = im.crop((0, (im.size[1]-im.size[0]) // 2, 
							im.size[0], (im.size[1]+im.size[0]) // 2))
				else :
					tmp = im.crop(((im.size[0]-im.size[1]) // 2, 0, 
								(im.size[0]+im.size[1]) // 2, im.size[1]))
				tmp.thumbnail((i[0], i[1]))
			tmp.save(path_new)

	def presentation_find_by_aid(src, aid, size, number=10) :
		'获得最新10张分享的照片，size 不可以为空'
		attach_qry = ShareSnap.image_list_by_aid(src, aid)
		attach_list = []
		for i in attach_qry :
			if len(attach_list) >= number :
				break
			link = ShareSnap.thumbnail_find(i.attach_uuid, size, i.second_uuid)
			if link :
				attach_list.append({
					'link': link, 
					'title': i.name_raw, 
				})
		return attach_list

	def archive_create(suid) :
		'创建压缩文件，返回错误信息(是否致命, 内容)'
		share = ShareSnap.share_find_by_uuid(suid)
		if not share :
			return True, '找不到分享'
		qry = ShareSnap.attach_find_by_uuid(suid)
		if ShareSnap.size_calc(qry) >= 128 * (1024 ** 2) :
			# 务必在计算 .count() 前完成，否则会没有计算每个文件的大小
			return True, '压缩包太大'
		if qry.count() <= 1 :
			return True, '仅仅压缩一个文件或者没有分享文件'
		if qry.filter(category='archive').exists() :
			return False, '已经创建压缩包'
		aid = share.account_id
		src = share.relation
		fname = AccountSnap.fname_find_by_aid(src, aid)
		sname = AccountSnap.sname_find_by_aid(src, aid)
		asname = '[%03d][%s][%s].zip' % (aid, sname, suid)
		afname = '[%03d][%s][%s].zip' % (aid, fname, suid)
		apath = os.path.join(settings.MEDIA_ROOT, 'archives', asname)
		with ZipFile(apath, 'w') as arc:
			for i in qry :
				sname = AccountSnap.sname_find_by_aid(i.relation, i.account_id)
				file_path = os.path.join \
							(settings.MEDIA_ROOT, 'files', sname, i.name_new)
				arc.write(file_path, arcname=i.name_raw)
		ShareAttach(attach_uuid=suid, shared=1, video_status=2, 
					account_id=aid, relation=src, category='archive', 
					name_new=asname, name_raw=afname).save()
		return False, ''

class ShareDicts :
	def club_admin(club, base_dict):
		dict_share = {}
		dict_share['inc_list'] = base_dict['inc_list']
		#dict_share['inc_list'].append({'name': 'club_prv_share',})
		return dict_share
		
	def share_show(suid) :
		from quan_event.views import EventSnap
		share = ShareSnap.share_find_by_uuid(suid)
		if not share :
			raise Http404()
		src = share.relation
		aid = share.account_id
		dict_render = {
			'data': share, 
			'share_content': share.content.split('\n'), 
			'visitors': AccountSnap.visit_count_by_account(share), 
		}
		dict_render['sname'] = AccountSnap.sname_find_by_aid(share.relation, 
								share.account_id)
		dict_render['fname'] = AccountSnap.fname_find_by_aid(share.relation, 
								share.account_id)
		date, time = ChineseSnap.datetime_comp(share.time_create)
		dict_render['time'] = date + ' ' + time
		dict_render['avatar'] = AvatarSnap.avatar_find(src, aid)
		dict_render['file_list'] = ShareSnap.file_list_find_by_suid(suid)
		dict_render['image_list'] = ShareSnap.image_list_find_by_suid(suid)
		dict_render['stream_list'] = ShareSnap.stream_list_find_by_suid(suid)
#		dict_render['chat_list'] = ShareSnap.chat_find(share.id)
		dict_render['title'] = t_(' - %s - %s的分享') % (share.subject, 
								dict_render['fname'])
		archive_qry = ShareAttach.objects.filter \
			(attach_uuid=suid, category='archive')
		if archive_qry :
			dict_render['archive_size'] = ChineseSnap.byte_exchange \
				(archive_qry[0].size)
		return dict_render

class ShareViews:
	@vary_on_cookie
	@UserAuthority.logged_in
	def share_create(request):
		dict_render = UserAgentSnap.record(request)
		if request.method == 'POST':
		#	json_dict = json.loads(request.POST.get('data', ''))
			src = request.POST.get('src', '')
			aid = int(request.POST.get('aid', -1))
			if not src or aid == -1 :	#假设是用户投递
				src = 'user'
				aid = UserSnap.uid_find_by_request(request)
			else :	#club
				json_dict = json.loads(request.POST.get('data', ''))
			UserAuthority.assert_permission(request, src, aid, True, True)
			if ShareSnap.share_frequent(src, aid) == False :
				raise Snap.error('分享频率过高。')
			if ShareSnap.limit_check(src, aid) == False :
				raise Snap.error('今天的分享数量已到上限。')
		#	eform = ShareInfoForm(json_dict)
		#	if not eform.is_valid():
			subject = request.POST.get('subject', '')
			content = request.POST.get('content', '')
			if not subject or len(subject) > 26 or len(content) > 1333 :
		#		logger.error(eform.errors)
				raise Snap.error('分享内容不完整或字数过多。')
		#	einst = eform.save(commit=False)
			einst = ShareInfo \
				(subject=subject, content=content, category='message')
			if src == 'user' :
				pass
			elif src == 'club' :
				if not 'category' in json_dict or json_dict['category'] == '' :
					if request.POST.get('category', '') :
						einst.category = request.POST.get('category', '')
					else :
						raise Snap.error('分享内容不完整。')
				else :
					einst.category = json_dict['category']
			else :
				raise Snap.error('似乎在对我做一些不好的事情')
			einst.account_id = aid
			einst.relation = src
			attach_uuid = request.POST.get('attach_uuid', '')
			if attach_uuid :
				einst.attach_uuid = attach_uuid
				if not ShareSnap.attach_find_by_uuid(attach_uuid).exists() :
					raise Snap.error('无法找到这个AttachID')
				if ShareSnap.share_find_by_uuid(attach_uuid) :
					raise Snap.error('附件已被分享')
			else :
				attach_uuid = ShareSnap.uuid_create()
				einst.attach_uuid = attach_uuid
			einst.password = request.POST.get('password', '')
			einst.content = content
			einst.save()
			msg_type = 'share-push'
			if not einst.password :
				if src == 'club' :
					if einst.category == 'knowledge' :
						PublicMessageAction.save(request, 'share', 'knowledge', 
							aid, src, einst.id, 'share')
					else :
						PublicMessageAction.save(request, 'share', 'new', aid,
							src, einst.id, 'share')
					PrivateMessageAction.save('新分享 - %s' % einst.subject, 
						einst.id, 'share', aid, src, aid, src)
					PrivateMessageAction.follower_send \
						(aid, '%s创建了新分享' % ClubSnap.fname_find_by_cid(aid), 
						einst.id, 'share')
				else :
					try :
						recv_src = request.POST.get('recv_src', '')
						recv_id = int(request.POST.get('recv_id', '0'))
						if recv_src == 'club' :
							account = ClubSnap.club_find_by_cid(recv_id)
						elif recv_src == 'user' :
							account = UserSnap.user_find_by_uid(recv_id)
						else :
							account = None
						if not account :
							raise ValueError
					except ValueError :
						raise Snap.error('找不到收件人')
					PrivateMessageAction.save(einst.subject, einst.id, 'share', 
						recv_id, recv_src, aid, src)
			if attach_uuid and src == 'club' :
				ShareSnap.mix_create(aid)
			QrcodeSnap.qrcode_create(attach_uuid, 'share')
			ShareSnap.archive_create(attach_uuid)
			ShareSnap.size_calc(ShareAttach.objects.filter \
								(attach_uuid=attach_uuid, category='archive'))
			CacheSnap.share_created(src, aid, attach_uuid)
			return Snap.success(request, t_('<strong><a href="/share/%s/">[%s]'
					'</a></strong> 已成功创建分享') % (attach_uuid, attach_uuid), 
					{ 'no_prefix': True, 'fade': 'false' })
		raise Http404()

	@vary_on_cookie
	def share_show(request, suid) :
		dict_render = UserAgentSnap.record(request)
		if request.method == 'GET' :
			dict_render.update(ShareDicts.share_show(suid))
			if 'Android' in request.META.get('HTTP_USER_AGENT', '') :
				dict_render['Android'] = True
			qry = dict_render['data']
			dict_render['leader'] = AccountSnap.aid_verify \
				(request, qry.relation, qry.account_id, False)
			dict_render['title'] = t_(' - %s') % dict_render['data'].subject
			return Snap.render('share_view.html', dict_render)
		else :
			qry = ShareSnap.share_find_by_uuid(suid)
			if not qry :
				raise Http404("或许已被删除")
			src = qry.relation
			aid = qry.account_id
			UserAuthority.assert_permission(request, src, aid, vice=False)
			qry.status = 1
			qry.save()
			MessageSnap.message_delete('share', qry.id)
			return Snap.success(request, '成功删除分享', { 'redirect': 
				'/%s/%s/' % (src, AccountSnap.sname_find_by_aid(src, aid)) })

	@vary_on_cookie
	@UserAuthority.logged_in
	def attach_create(request):
		dict_render = UserAgentSnap.record(request)
		if request.method != 'POST' :
			# 已经无用（会出错）
			dict_render['title'] = ' - 上传附件'
			return Snap.render('attach_upload.html', dict_render)
		# POST
		files = request.FILES.getlist('multiple-file')
		src = 'user'
		aid = UserSnap.uid_find_by_request(request)
		attach_uuid = ShareSnap.uuid_create()
		ShareSnap.muti_create(files, src, aid, attach_uuid)
		progress_id = request.GET.get('X-Progress-ID')
		if not progress_id :
			raise Snap.error('找不到进程ID')
		cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
		if cache.get("loading_" + cache_key) :
			cache.delete("loading_" + cache_key)
			cache.set("loaded_" + cache_key, attach_uuid)
		return Snap.success(request, '文件上传成功')

	@vary_on_cookie
	def attach_download(request) :
		dict_render = UserAgentSnap.record(request)
		if not request.user.is_authenticated() and \
			not UserAgentSnap.ua_check(request) :
			raise Http403('服务器认为只有登录用户才能访问')
		tid = request.GET.get('tid', '')
		suid = request.GET.get('uuid', '')
		arc = request.GET.get('type', '')
		fraw, fdir = ShareSnap.download_find(suid, tid, arc)
		return Snap.file(request, fdir, fraw)

	@vary_on_cookie
	@UserAuthority.logged_in
	def chat_create(request) :
		dict_render = UserAgentSnap.record(request)
		if request.method == 'POST' :
			uid = UserSnap.uid_find_by_request(request)
			suid = request.POST.get('suid', '')
			cont = request.POST.get('context', '')
			if not ShareSnap.chat_frequent(uid, suid) :
				raise Snap.error('评论频率过高')
			sid = ShareSnap.sid_find_by_uuid(suid)
			if not sid :
				raise Snap.error('投递错误')
				# 目前 share 的 chat 功能被移到新闻模块，但是还有很多地方需要更改
			if ShareSnap.chat_save(sid, cont, uid) == True :
				fname = UserSnap.fname_find_by_request(request)
				return Snap.success(request, '很顺利地添加了评论', 
									{ 'reload': True })
			else :
				raise Snap.error('似乎输入为空')
		else :
			raise Http404()

	@never_cache
	def uuid_get(request) :
		'''
			1.判断cache是否存在
			2.生成uuid
			3.销毁cache
		'''
		dict_render = UserAgentSnap.record(request)
		progress_id = request.POST.get('X-Progress-ID')
		if progress_id:
			cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
			attach_uuid = cache.get('loaded_' + cache_key)
			if attach_uuid :
				cache.delete('loaded_' + cache_key)
				return Snap.success(request, '文件上传成功', 
									{ 'attach_uuid': attach_uuid })
		raise Snap.error('发生未知错误，请重试或联系HCC')

	@never_cache
	def progress_find(request):
		"""
			Return JSON object with information about the progress of an upload.
		"""
		dict_render = UserAgentSnap.record(request)
		progress_id = request.POST.get('X-Progress-ID')
		if progress_id:
			cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
			data = cache.get('loading_' + cache_key)
#			logger.error("cak " + cache_key + " data " + str(data))
			return Snap.success(request, '', { 'q': data })
		else:
			raise Snap.error('找不到进程ID')

class ShareSiteMap(Sitemap) :
	def items(self) :
		return ShareInfo.objects.filter(status=0, relation='club')
	def location(self, item) :
		return '/share/%s/' % item.attach_uuid


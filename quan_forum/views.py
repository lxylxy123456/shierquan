from .models import *
from quan_share.models import *

from quan_account.views import *
from quan_auth.views import AuthDicts
from quan_avatar.views import AvatarSnap
from quan_event.views import EventSnap
from quan_message.views import MessageSnap
from quan_share.views import ShareSnap
from quan_ua.views import *

class ForumSnap :
	def group_all() :
		return ForumGroup.objects.filter(status=0)

	def thread_find_by_gid(gid) :
		return ForumThread.objects.filter(status=0, group_id=gid)

	def group_find_by_gid(gid) :
		try :
			return ForumGroup.objects.get(status=0, id=gid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def sname_find_by_gid(gid) :
		try :
			return ForumGroup.objects.get(status=0, id=gid).simp_name
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def fname_find_by_gid(gid) :
		try :
			return ForumGroup.objects.get(status=0, id=gid).subject
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def group_find_by_sname(sname) :
		try :
			return ForumGroup.objects.get(status=0, simp_name=sname)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def gid_find_by_sname(sname) :
		try :
			return ForumGroup.objects.get(status=0, simp_name=sname).id
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def response_find_by_rid(rid) :
		try :
			return ForumResponse.objects.get(status=0, id=rid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def response_find_by_thid(thid) :
		return ForumResponse.objects.filter \
					(status=0, thread_id=thid).order_by('time_create')

	def thread_find_by_thid(thid, gid=None) :
		'如果gid(group_id)可用，会进行检测'
		try :
			if gid :
				return ForumThread.objects.get(status=0, id=thid, group_id=gid)
			else :
				return ForumThread.objects.get(status=0, id=thid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def thid_find_by_rid(rid) :
		try :
			return ForumResponse.objects.get(status=0, id=rid).thread_id
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def gid_find_by_thid(thid) :
		try :
			return ForumThread.objects.get(id=thid, status=0).group_id
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def sname_validate(sname) :
		'验证last_name是否有效'
		m = re.match('([a-zA-Z\-]+)$', sname)
		if not m :
			raise Snap.error('请使用小写字母和连线符组合链接 如：test-forum')
		if ForumGroup.objects.filter(status=0, simp_name=sname).exists() :
			raise Snap.error('链接已被注册')

	def forum_admin_verify(request) :
		'HCC正社长'
		return ClubSnap.sname_verify(request, 'hcc-computer-community', False) \
			or ClubSnap.sname_verify(request, 'club-union', False)

	def forum_core_verify(request, group) :
		'社联核心成员'
		return group.account_id == request.user.id or \
				ClubSnap.sname_verify(request, 'club-union', True, True)

	def group_admin_verify(request, gid) :
		'是否是group的管理员'
		if ForumSnap.forum_admin_verify(request) :
			return True
		qry = ForumGroup.objects.filter(status=0, id=gid)
		return qry and AccountSnap.aid_verify \
								(request, qry[0].relation, qry[0].account_id)

	def admin_verify(src, aid, request) :
		'''
			计算删除权限
			src in ('group', 'thread', 'response')
			rules :
				HCC head is super admin
				thread 		creator / group owner
				response	creator / group owner
		'''
		if ForumSnap.forum_admin_verify(request) :
			return True
		if src == 'thread' :
			qry = ForumSnap.thread_find_by_thid(aid)
			if not qry :
				return False
			if AccountSnap.aid_verify(request, qry.send_relation, qry.send_id) :
				return True
			return ForumSnap.group_admin_verify(request, qry.group_id)
		elif src == 'response' :
			qry = ForumSnap.response_find_by_rid(aid)
			if not qry :
				return False
			if AccountSnap.aid_verify(request, qry.send_relation, qry.send_id) :
				return True
			gid = ForumSnap.gid_find_by_thid(qry.thread_id)
			if gid :
				return ForumSnap.group_admin_verify(request, gid)
			else :
				return False
		return False

	def edit_verify(src, request, qry) :
		'''
			计算有权利更改的用户
			src in ('group', 'thread', 'response') 指向要更改的对象
			方法：
				group		Group owner
				thread		Thread owner
				response	Core owner
		'''
		if src == 'group' :
			return AccountSnap.aid_verify(request, qry.relation, qry.account_id)
		else :
			return AccountSnap.aid_verify \
						(request, qry.send_relation, qry.send_id)

	def creator_verify(src, request, thid=0, gid=0) :
		'''
			计算有权利创建的用户
			src in ('group', 'thread', 'response') 指向要添加的对象
			gid 和 thid 在 src = response 时有效
			rules :
				group		HCC head
				thread		anyone
				response	anyone					# group.secret = False
							HCC core & thread owner	# group.secret = True
		'''
		if not request.user.is_authenticated() :
			return False
		if src == 'group' :
			return ForumSnap.forum_admin_verify(request)
		elif src == 'thread' :
			return True
		elif src == 'response' :
			qry = ForumSnap.thread_find_by_thid(thid, gid)
			if not qry :				# 找不到
				return False
			if not gid :
				gid = qry.group_id
			group_qry = ForumSnap.group_find_by_gid(gid)
			if not group_qry :			# 找不到
				return False
			if not group_qry.secret :	# 非私密论坛
				return True
			return AccountSnap.aid_verify \
						(request, qry.send_relation, qry.send_id) or \
					ForumSnap.forum_core_verify(request, group_qry)
		else :
			return False

	def view_verify(src, request, thid=0, gid=0) :
		'''
			计算有权利查看的用户
			src in ('group', 'thread') 指向要查看的对象
			gid 和 thid 在 src = response 时有效
			rules :
				group		anyone
				thread		anyone					# group.secret = False
							HCC core & thread owner	# group.secret = True
				response	anyone					# group.secret = False
							HCC core & thread owner	# group.secret = True
		'''
		if src == 'group' :
			return ForumSnap.forum_admin_verify(request)
		elif src in ('thread', 'response') :
			qry = ForumSnap.thread_find_by_thid(thid, gid)
			if not qry :				# 找不到
				return False
			if not gid :
				gid = qry.group_id
			group_qry = ForumSnap.group_find_by_gid(gid)
			if not group_qry :			# 找不到
				return False
			if not group_qry.secret :	# 非私密论坛
				return True
			return AccountSnap.aid_verify \
						(request, qry.send_relation, qry.send_id) or \
					ForumSnap.forum_core_verify(request, group_qry)
		else :
			return False

	def url_find_by_thread(thread) :
		group_sname = ForumSnap.sname_find_by_gid(thread.group_id)
		return '/forum/%s/%d/' % (group_sname, thread.id)

	def attach_wrap(suid) :
		'通过 qry 中的 attach_uuid 找到附件并计算 dict_render'
		if not suid :
			return []
		if not ShareInfo.objects.filter(attach_uuid=suid, status=0).exists() :
			return []
		qry = ShareAttach.objects.filter(attach_uuid=suid)
		attach_list = []
		for index, i in enumerate(qry, 1) :
			url = ShareSnap.url_find_by_attach(i)
			attach_list.append({
				'url': url, 
				'data': i, 
				'name': i.name_raw, 
				'thumbnail': ShareSnap.thumbnail_find \
											(suid, 'exlarge', i.second_uuid), 
				'index2': index % 2, 
				'index3': index % 3, 
				'index4': index % 4, 
			})
		return attach_list

	def public_thread_list() :
		'返回所有公共帖子'
		group_qry = ForumGroup.objects.filter(status=0, secret=0)
		gid_list = group_qry.values_list('id', flat=True)
		return ForumThread.objects.filter(status=0, group_id__in=gid_list)

	def thread_latest_render() :
		'渲染最新的帖子（用于侧边栏渲染）'
		thread_latest = []
		for i in ForumSnap.public_thread_list().order_by('-time_update')[:3] :
			thread_latest.append({
				'data': i, 
				'url': ForumSnap.url_find_by_thread(i), 
			})
		return thread_latest

class ForumViews :
	@vary_on_cookie
	def forum_show(request) :
		"显示主题列表"
		dict_render = UserAgentSnap.record(request)
		topic_dict = {}
		dict_render['is_admin'] = ForumSnap.forum_admin_verify(request)
		for i in ForumSnap.group_all() :
			if i.topic not in topic_dict :
				topic_dict[i.topic] = []
			thread_num = 0
			resp_num = 0 # thread + resonse
			today_num = 0
			latest = i.time_update
			now = datetime.now()
			today = datetime(now.year, now.month, now.day)
			for j in ForumSnap.thread_find_by_gid(i.id) :
				thread_num += 1
				resp_num += 1 + j.response_number
				if latest < j.time_update :
					latest = j.time_update
				if j.time_update >= today :
					today_num += 1
			topic_dict[i.topic].append({
				'data': i, 
				'thread': thread_num, 
				'resp': resp_num, # thread + resonse
				'last': ChineseSnap.timedelta_simp(now - latest), 
				'today': today_num, 
				'avatar': AvatarSnap.avatar_find \
											('forum', i.id, 'medium', True), 
			})
		dict_render['topic_list'] = topic_dict.items()
		dict_render['thread_latest'] = ForumSnap.thread_latest_render()
		dict_render['title'] = ' - 论坛'
		return Snap.render('forum_home.html', dict_render)

	@vary_on_cookie
	def group_show(request, sname) :
		"显示单个主题"
		dict_render = UserAgentSnap.record(request)
		qry = ForumSnap.group_find_by_sname(sname)
		if not qry :
			raise Http404()
		dict_render['data'] = qry
		dict_render['avatar'] = AvatarSnap.avatar_find \
										('forum', qry.id, 'large', True)
		dict_render['is_admin'] = ForumSnap.group_admin_verify(request, qry.id)
		thread_qry = ForumSnap.thread_find_by_gid(qry.id)
		if qry.secret and not ForumSnap.forum_core_verify(request, qry) :
			thread_qry = thread_qry.filter \
								(send_id=request.user.id, send_relation='user')
		thread_qry = thread_qry.order_by('-time_update')
		sliced_qry = AuthDicts.page_dict(request, thread_qry, 20, dict_render)
		dict_render['thread_list'] = []
		for i in sliced_qry :
			dict_render['thread_list'].append({
				'data': i, 
				'time_update': ChineseSnap.datetime_simp(i.time_update), 
				'send_nickname': AccountSnap.nickname_find_by_aid \
					(i.send_relation, i.send_id), 
				'reply_number': ForumSnap.response_find_by_thid(i.id).count(), 
			})
		dict_render['thread_latest'] = ForumSnap.thread_latest_render()
		dict_render['title'] = t_(' - %s') % qry.subject
		return Snap.render('forum_group.html', dict_render)

	@vary_on_cookie
	def thread_show(request, sname, thid) :
		"显示单个帖子"
		dict_render = UserAgentSnap.record(request)
		try :
			thid = int(thid)
		except ValueError :
			raise Http404()
		group_qry = ForumSnap.group_find_by_sname(sname)
		if not group_qry :
			raise Http404()
		qry = ForumSnap.thread_find_by_thid(thid, group_qry.id)
		if not qry :
			raise Http404()
		if not ForumSnap.view_verify('thread', request, thid, group_qry.id) :
			raise Http403('您没有权限查看本页面')
		dict_render['group_data'] = group_qry
		dict_render['thread_data'] = qry
		is_admin = ForumSnap.forum_admin_verify(request) or \
					ForumSnap.group_admin_verify(request, qry.group_id)
		attach_list = ForumSnap.attach_wrap(qry.attach_uuid)
		dict_thread = {
			'data': qry, 
			'relation': 'thread', 
			'level': 0, 
			'time_create': ChineseSnap.datetime_simp(qry.time_create), 
			'avatar': AvatarSnap.avatar_all(qry.send_relation, qry.send_id), 
			'nickname': UserSnap.nickname_find_by_uid(qry.send_id), 
			'sname': UserSnap.sname_find_by_uid(qry.send_id), 
			'attach': attach_list, 
			'attach_len': len(attach_list), 
			'attach_uuid': qry.attach_uuid, 
			'can_delete': is_admin or qry.send_id == request.user.id, 
		}
		# 计算 response_list: 根据回复排序
		response_qry = ForumSnap.response_find_by_thid(thid) \
								.filter(reply_relation='thread')
		dict_render['response_list'] = [dict_thread]
		
		try :
			rid = int(request.GET.get('response', '0'))
			i = list(response_qry.values_list('id', flat=True)).index(rid)
			index = i // 10 + 1
		except ValueError :
			index = None
		for i in AuthDicts.page_dict \
							(request, response_qry, 10, dict_render, index) :
			children_list = []
			for j in ForumSnap.response_find_by_thid(thid) \
							.filter(reply_relation='response', reply_id=i.id) :
				children_list.append({
					'data': j, 
					'relation': 'response', 
					'time_create': ChineseSnap.datetime_simp(j.time_create), 
					'avatar': AvatarSnap.avatar_all(j.send_relation, j.send_id),
					'nickname': UserSnap.nickname_find_by_uid(j.send_id), 
					'sname': UserSnap.sname_find_by_uid(j.send_id), 
					'can_delete': is_admin or j.send_id == request.user.id, 
				})
			dict_render['response_list'].append({
				'data': i, 
				'relation': 'response', 
				'level': 0, 
				'time_create': ChineseSnap.datetime_simp(i.time_create), 
				'avatar': AvatarSnap.avatar_all(i.send_relation, i.send_id), 
				'nickname': UserSnap.nickname_find_by_uid(i.send_id), 
				'sname': UserSnap.sname_find_by_uid(i.send_id), 
				'attach': attach_list, 
				'attach_len': len(attach_list), 
				'attach_uuid': i.attach_uuid, 
				'children_list': children_list, 
				'can_delete': is_admin or i.send_id == request.user.id, 
			})
		dict_render['thread_latest'] = ForumSnap.thread_latest_render()
		dict_render['title'] = t_(' - %s') % qry.subject
		return Snap.render('forum_thread.html', dict_render)

	@vary_on_cookie
	@UserAuthority.logged_in
	def thread_post(request, sname, tid='') :
		'''
			发表或编辑内容
			可能情况
				action	src			aid		reply
				new		group				-
				new		thread				group_sname
				new		response			(thread / response), aid
				edit	group		sname
				edit	thread		thid
				edit	response	rid
		'''
		from quan_news.views import NewsSnap
		dict_render = UserAgentSnap.record(request)
		# 处理参数
		action = request.POST.get('action') or request.GET.get('action')
		relation = request.POST.get('relation') or request.GET.get('relation')
		try :
			reply_aid = int(request.POST.get('reply_aid', '0'))
			aid = int(request.GET.get('aid') or request.POST.get('aid', '0'))
		except ValueError :
			raise Http404('参数错误')
		# 寻找数据
		if action == 'new' :
			if relation == 'group' :
				thid, gid = None, None		# 填表需要
				subject_required = True
				dict_render['page_title'] = '创建板块'
			elif relation == 'thread' :
				group_qry = ForumSnap.group_find_by_sname(sname)
				if not group_qry :
					raise Http404('找不到群组')
				thid, gid = None, group_qry.id
				subject_required = True
				dict_render['page_title'] = '发表帖子'
			elif relation == 'response' :
				thid = reply_aid
				gid = ForumSnap.gid_find_by_thid(thid)
				if not gid or not thid :
					raise Http404('参数错误')
				group_qry = ForumSnap.group_find_by_gid(gid)
				subject_required = False
				dict_render['page_title'] = '发表回复'
			else :
				raise Http404('参数错误')
			if not ForumSnap.creator_verify(relation, request, thid, gid) :
				raise Snap.error('您没有权限')
			qry = None
		elif action == 'edit' :
			if relation == 'group' :
				qry = ForumSnap.group_find_by_sname(sname)
				subject_required = True
				aid = qry.id
				dict_render['page_title'] = '编辑板块信息'
				dict_render['data_account_sname'] = UserSnap.sname_find_by_uid \
																(qry.account_id)
			elif relation == 'thread' :
				raise Http404('功能已被禁用')
				qry = ForumSnap.thread_find_by_thid(aid)
				subject_required = True
				dict_render['page_title'] = '编辑帖子'
			elif relation == 'response' :
				raise Http404('功能已被禁用')
				qry = ForumSnap.response_find_by_rid(aid)
				subject_required = False
				dict_render['page_title'] = '编辑回复'
			else :
				raise Http404('参数错误')
			if not qry :
				raise Http404('找不到对象')
			if not ForumSnap.edit_verify(relation, request, qry) :
				if relation == 'group' and \
					ForumSnap.forum_admin_verify(request) :
					pass	# 允许特权用户
				else :
					raise Snap.error('您没有权限')
		else :
			raise Http404('参数错误')
		# 如果不是提交，渲染模板
		if request.method != 'POST' :
			dict_render['action'] = action
			dict_render['relation'] = relation
			dict_render['reply_aid'] = reply_aid
			dict_render['aid'] = aid
			dict_render['data'] = qry
			dict_render['subject_required'] = subject_required
			group_qry = ForumSnap.group_find_by_sname(sname)
			if action == 'new' and relation == 'group' :
				dict_render['group_data'] = {
					'subject': '创建', 
					'simp_name': '-', 
				}
			elif not group_qry :
				raise Http404()
			else :
				dict_render['group_data'] = group_qry
			if action == 'new' and relation == 'thread' :
				dict_render['title'] = ' - 发表帖子'
				dict_render['attach_allowed'] = True
			else :
				dict_render['title'] = ' - 创建板块'
			dict_render['thread_latest'] = ForumSnap.thread_latest_render()
			return Snap.render('forum_post.html', dict_render)
		# 标题和内容
		try :
			json_data = json.loads(request.POST.get('data', ''))
		except json.decoder.JSONDecodeError :
			raise Snap.error('数据已损坏')
		subject = json_data.get('subject', '')
		content = json_data.get('content', '')
		if (subject_required and not subject) or not content :
			raise Snap.error('标题或内容不全')
		if not NewsSnap.html_script_filter(content) :
			raise Snap.error('内容中包含非法字符')
		# 创建 qry
		if action == 'new' :
			if relation == 'group' :
				qry = ForumGroup(relation='user', subject=subject, 
								content=content)
			elif relation == 'thread' :
				qry = ForumThread(send_id=request.user.id, 
								send_relation='user', subject=subject, 
								content=content, group_id=gid)
			else :	# relation == 'response'
				qry = ForumResponse(send_id=request.user.id, 
								send_relation='user', reply_id=reply_aid, 
								reply_relation='thread', content=content, 
								thread_id=thid)
		else :	# action == 'edit'
			if relation == 'group' :
				history = ForumHistory(relation='group', account_id=qry.id, 
									subject=qry.subject, content=qry.content)
				qry.subject = subject
				qry.content = content
			elif relation == 'thread' :
				history = ForumHistory(relation='thread', account_id=qry.id, 
									subject=qry.subject, content=qry.content)
				qry.subject = subject
				qry.content = content
			else :	# relation == 'response'
				history = ForumHistory(relation='response', account_id=qry.id, 
														content=qry.content)
				qry.content = content
		# 用户组控制的其他参数
		if relation == 'group' :
			# Secret
			secret = json_data.get('secret')
			if secret not in ('0', '1') :
				raise Snap.error('请选择论坛是否私密')
			qry.secret = secret == '1'
			# Topic
			qry.topic = json_data.get('topic')
			if not qry.topic :
				raise Snap.error('请输入论坛所属群组')
			# Simp name
			simp_name = json_data.get('simp_name', '')
			if qry.simp_name != simp_name :
				ForumSnap.sname_validate(simp_name)
				qry.simp_name = simp_name
			# Account id
			uid = UserSnap.uid_find_by_sname(json_data.get('admin', ''))
			if not uid :
				raise Snap.error('请输入正确的用户链接')
			qry.account_id = uid
		# 附件
		attach_uuid = request.POST.get('attach_uuid')
		if attach_uuid :
			if action != 'new' or relation not in ('thread', 'response') :
				raise Snap.error('[附件] 不允许的操作')
			qry.attach_uuid = attach_uuid
			if not ShareSnap.attach_find_by_uuid(attach_uuid).exists() :
				raise Snap.error('[附件] 无法找到这个AttachID')
			if ShareSnap.share_find_by_uuid(attach_uuid) :
				raise Snap.error('附件已被分享')
			if subject :
				subj = subject + ' 的附件'
			else :
				subj = '论坛回复附件'
			share_qry = ShareInfo(subject=subj, account_id=request.user.id, 
									relation='user', attach_uuid=attach_uuid)
		# 保存
		try :
			qry.save()
		except DataError :
			raise Snap.error('标题或内容过长')
		# 保存 history
		if action == 'edit' :
			try :
				history.save()
			except DataError :
				logger.error('error in forum when saving history. ')
		# 保存 share
		if attach_uuid :
			try :
				share_qry.save()
				ShareSnap.archive_create(attach_uuid)
			except DataError :
				logger.error('error in forum when saving share_qry. ')
		# 维护数据库
		if action == 'new' and relation == 'response' :
			thread = ForumSnap.thread_find_by_thid(thid)
			if thread :
				thread.response_number += 1
				thread.save()
		# 返回消息
		if relation == 'group' :
			url = '/forum/%s/' % qry.simp_name
			if action == 'new' :
				comment = '成功创建板块'
			else :
				comment = '成功编辑板块信息'
		elif relation == 'thread' :
			url = '/forum/%s/%d/' % (sname, qry.id)
			if action == 'new' :
				if not group_qry.secret :
					PublicMessageAction.save(request, 'forum', 'thread', 
											request.user.id, 'user', 
											qry.id, 'forum_thread')
				comment = '发帖成功'
			else :
				comment = '成功编辑帖子'
		else :	# relation == 'response'
			url = '/forum/%s/%d?response=%d#response-%d' % \
								(sname, qry.thread_id, qry.id, qry.id)
			if action == 'new' :
				if not group_qry.secret :
					PublicMessageAction.save(request, 'forum', 'response', 
											request.user.id, 'user', 
											qry.id, 'forum_response')
				comment = '回复成功'
			else :
				comment = '成功编辑回复'
		return Snap.success(request, comment, { 'redirect': url })

	@vary_on_cookie
	@UserAuthority.logged_in
	def thread_chat(request, sname, tid) :
		'添加 chat'
		if request.method != 'POST' :
			raise Http404()
		try :
			rid = int(request.POST.get('rid', '0'))
			tid = int(tid)
		except ValueError :
			raise Http404('参数错误')
		resp = ForumSnap.response_find_by_rid(rid)
		if not resp or resp.thread_id != tid or resp.reply_relation != 'thread':
			raise Http404('关系错误')
		content = request.POST.get('content', '')
		if not content :
			raise Snap.error('内容为空')
		if len(content) > 300 :
			raise Snap.error('内容太长')
		qry = ForumResponse(send_id=request.user.id, send_relation='user', 
							reply_id=rid, reply_relation='response', 
							content=content, thread_id=tid)
		try :
			qry.save()
		except Dataerror :
			raise Snap.error('数据太长')
		return Snap.success(request, '发表成功', { 'reload': True, 'rid': qry.id,
					'nickname': UserSnap.nickname_find_by_uid(request.user.id)})

	@vary_on_cookie
	def forum_delete(request, sname) :
		'删除论坛的内容'
		dict_render = UserAgentSnap.record(request)
		if request.method != 'POST' :
			return Snap.redirect('/forum/%s/' % sname)
		relation = request.POST.get('relation')
		try :
			aid = int(request.POST.get('aid', '0'))
		except ValueError :
			raise Http404('数据错误')
		if not relation or not aid :
			raise Snap.error('参数不完整')
		if not ForumSnap.admin_verify(relation, aid, request) :
			raise Http403('您没有权限')
		if relation == 'group' :
			raise Snap.error('请求被拒绝，请联系HCC社团以实现')
		elif relation == 'thread' :
			thread = ForumSnap.thread_find_by_thid(aid)
			thread.status = 1
			thread.save()
			response = ForumSnap.response_find_by_thid(aid)
			rid_list = zip(itertools.repeat('forum_response'), 
							response.values_list('id', flat=True))
			response.update(status=1)
			MessageSnap.message_delete('forum_thread', aid)
			collections.deque(itertools.starmap(MessageSnap.message_delete, 
												rid_list), 0)
			return Snap.success(request, '删除成功', 
								{ 'redirect': '/forum/%s/' % sname })
		elif relation == 'response' :
			response = ForumSnap.response_find_by_rid(aid)
			response.status = 1
			response.save()
			rlist = ForumResponse.objects.filter(status=0, reply_id=aid, 
												reply_relation='response')
			rlist.update(status=1)
			MessageSnap.message_delete('forum_response', aid)
			return Snap.success(request, '删除成功', { 'reload': True })
		else :
			raise Snap.error('参数错误')

	@vary_on_cookie
	def random(request, *arguments) :
		dict_render = UserAgentSnap.record(request)
		thread_qry = ForumSnap.public_thread_list()
		thread_number = thread_qry.count()
		if not thread_number :
			return Snap.redirect('/forum/')
		index = random.randrange(thread_number)
		return Snap.redirect(ForumSnap.url_find_by_thread(thread_qry[index]))

class ForumSiteMap(Sitemap) :
	def items(self) :
		return ForumThread.objects.filter(status=0)
	def location(self, item) :
		return '/forum/%s/%d/' % \
				(ForumSnap.sname_find_by_gid(item.group_id), item.id)


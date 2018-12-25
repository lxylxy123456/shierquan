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

from .models import *
from quan_share.models import *

from quan_account.views import *
from quan_auth.views import AuthDicts
from quan_avatar.views import AvatarSnap
from quan_event.views import EventSnap
from quan_share.views import ShareSnap
from quan_ua.views import *

class ForumSnapOld :
	def group_all() :
		return ForumGroupOld.objects.filter(status=0)

	def thread_find_by_gid(gid) :
		return ForumThreadOld.objects.filter(status=0, group_id=gid)

	def group_find_by_gid(gid) :
		try :
			return ForumGroupOld.objects.get(status=0, id=gid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def sname_find_by_gid(gid) :
		try :
			return ForumGroupOld.objects.get(status=0, id=gid).simp_name
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def fname_find_by_gid(gid) :
		try :
			return ForumGroupOld.objects.get(status=0, id=gid).subject
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def group_find_by_sname(sname) :
		try :
			return ForumGroupOld.objects.get(status=0, simp_name=sname)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def gid_find_by_sname(sname) :
		try :
			return ForumGroupOld.objects.get(status=0, simp_name=sname).id
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def response_find_by_rid(rid) :
		try :
			return ForumResponseOld.objects.get(status=0, id=rid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def response_find_by_thid(thid) :
		return ForumResponseOld.objects.filter \
					(status=0, thread_id=thid).order_by('time_create')

	def thread_find_by_thid(thid, gid=None) :
		'如果gid(group_id)可用，会进行检测'
		try :
			if gid :
				return ForumThreadOld.objects.get(status=0, id=thid, group_id=gid)
			else :
				return ForumThreadOld.objects.get(status=0, id=thid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def thid_find_by_rid(rid) :
		try :
			return ForumResponseOld.objects.get(status=0, id=rid).thread_id
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def gid_find_by_thid(thid) :
		try :
			return ForumThreadOld.objects.get(id=thid, status=0).group_id
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def sname_validate(sname) :
		'验证last_name是否有效'
		m = re.match('([a-zA-Z\-]+)$', sname)
		if not m :
			raise Snap.error('请使用小写字母和连线符组合链接 如：test-forum')
		if ForumGroupOld.objects.filter(status=0, simp_name=sname).exists() :
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
		if ForumSnapOld.forum_admin_verify(request) :
			return True
		qry = ForumGroupOld.objects.filter(status=0, id=gid)
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
		if ForumSnapOld.forum_admin_verify(request) :
			return True
		if src == 'thread' :
			qry = ForumSnapOld.thread_find_by_thid(aid)
			if not qry :
				return False
			if AccountSnap.aid_verify(request, qry.send_relation, qry.send_id) :
				return True
			return ForumSnapOld.group_admin_verify(request, qry.group_id)
		elif src == 'response' :
			qry = ForumSnapOld.response_find_by_rid(aid)
			if not qry :
				return False
			if AccountSnap.aid_verify(request, qry.send_relation, qry.send_id) :
				return True
			gid = ForumSnapOld.gid_find_by_thid(qry.thread_id)
			if gid :
				return ForumSnapOld.group_admin_verify(request, gid)
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
			return ForumSnapOld.forum_admin_verify(request)
		elif src == 'thread' :
			return True
		elif src == 'response' :
			qry = ForumSnapOld.thread_find_by_thid(thid, gid)
			if not qry :				# 找不到
				return False
			if not gid :
				gid = qry.group_id
			group_qry = ForumSnapOld.group_find_by_gid(gid)
			if not group_qry :			# 找不到
				return False
			if not group_qry.secret :	# 非私密论坛
				return True
			return AccountSnap.aid_verify \
						(request, qry.send_relation, qry.send_id) or \
					ForumSnapOld.forum_core_verify(request, group_qry)
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
			return ForumSnapOld.forum_admin_verify(request)
		elif src in ('thread', 'response') :
			qry = ForumSnapOld.thread_find_by_thid(thid, gid)
			if not qry :				# 找不到
				return False
			if not gid :
				gid = qry.group_id
			group_qry = ForumSnapOld.group_find_by_gid(gid)
			if not group_qry :			# 找不到
				return False
			if not group_qry.secret :	# 非私密论坛
				return True
			return AccountSnap.aid_verify \
						(request, qry.send_relation, qry.send_id) or \
					ForumSnapOld.forum_core_verify(request, group_qry)
		else :
			return False

	def replied(src, aid) :
		'是否被引用（不可以删除）'
		if src == 'group' :
			return ForumSnapOld.thread_find_by_gid(aid).exists()
		elif src == 'thread' :
			return ForumSnapOld.response_find_by_thid(aid).exists()
		elif src == 'response' :
			return ForumResponseOld.objects.filter(reply_id=aid, 
							reply_relation='response').exists()
		else :
			return False

	def url_find_by_thread(thread) :
		group_sname = ForumSnapOld.sname_find_by_gid(thread.group_id)
		return '/forum-old/%s/%d/' % (group_sname, thread.id)

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
		group_qry = ForumGroupOld.objects.filter(status=0, secret=0)
		gid_list = group_qry.values_list('id', flat=True)
		return ForumThreadOld.objects.filter(status=0, group_id__in=gid_list)

	def thread_latest_render() :
		'渲染最新的帖子（用于侧边栏渲染）'
		thread_list = ForumSnapOld.public_thread_list().order_by('-time_update')
		dict_render = { 'thread_latest': [] }
		for i in thread_list[:3] :
			dict_render['thread_latest'].append({
				'data': i, 
				'url': ForumSnapOld.url_find_by_thread(i), 
			})
		return dict_render

	def delete(src, aid) :
		'删除object，回复错误信息'
		# 判断依赖
		if ForumSnapOld.replied(src, aid) :
			raise Snap.error('内容已经被回复，无法删除')
		# 查找对象
		if src == 'group' :
			qry = ForumSnapOld.group_find_by_gid(aid)
		elif src == 'thread' :
			qry = ForumSnapOld.thread_find_by_thid(aid)
		elif src == 'response' :
			qry = ForumSnapOld.response_find_by_rid(aid)
		else :
			raise Snap.error('参数错误')
		if not qry :
			raise Snap.error('找不到对象')
		# 删除
		qry.delete()

	def recursive_delete(src, aid) :
		'递归删除，不包含权限判断，返回是否错误'
		int('a')	# 危险函数，已禁用
		thread_list = []
		response_list = []
		if src == 'thread' :
			thread_list = [aid]
		if src == 'response' :
			response_list = [aid]
		# begin deleting
		if src == 'group' :
			qry = ForumSnapOld.group_find_by_gid(aid)
			if not qry :
				return True
			qry.status = 1
			qry.save()
			for i in ForumSnapOld.thread_find_by_gid(aid) :
				thread_list.append(i.id)
		if thread_list :
			qry = ForumThreadOld.objects.filter(id__in=thread_list, status=0)
			if qry.count() != 1 and src == 'thread' :
				return True
			qry.update(status=1)
			for i in qry :
				for j in ForumResponseOld.objects.filter(thread_id=i.id) :
					response_list.append(j.id)
		if response_list :
			qry = ForumResponseOld.objects.filter(id__in=response_list, status=0)
			if qry.count() != 1 and src == 'response' :
				return True
			qry.update(status=1)
		return False

class ForumViewsOld :
	@vary_on_cookie
	def forum_show(request) :
		"显示主题列表"
		dict_render = UserAgentSnap.record(request)
		topic_dict = {}
		dict_render['is_admin'] = ForumSnapOld.forum_admin_verify(request)
		for i in ForumSnapOld.group_all() :
			if i.topic not in topic_dict :
				topic_dict[i.topic] = []
			thread_num = 0
			resp_num = 0 # thread + resonse
			today_num = 0
			latest = i.time_update
			now = datetime.now()
			today = datetime(now.year, now.month, now.day)
			for j in ForumSnapOld.thread_find_by_gid(i.id) :
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
		dict_render.update(ForumSnapOld.thread_latest_render())
		dict_render['title'] = ' - 旧版本论坛'
		return Snap.render('forum_old_home.html', dict_render)

	@vary_on_cookie
	def group_show(request, sname) :
		"显示单个主题"
		dict_render = UserAgentSnap.record(request)
		qry = ForumSnapOld.group_find_by_sname(sname)
		if not qry :
			raise Http404()
		dict_render['data'] = qry
		dict_render['avatar'] = AvatarSnap.avatar_find \
										('forum', qry.id, 'large', True)
		dict_render['is_admin'] = ForumSnapOld.group_admin_verify(request, qry.id)
		thread_qry = ForumSnapOld.thread_find_by_gid(qry.id)
		if qry.secret and not ForumSnapOld.forum_core_verify(request, qry) :
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
				'reply_number': ForumSnapOld.response_find_by_thid(i.id).count(), 
			})
		dict_render.update(ForumSnapOld.thread_latest_render())
		dict_render['title'] = t_(' - %s') % qry.subject
		return Snap.render('forum_old_group.html', dict_render)

	@vary_on_cookie
	def thread_show(request, sname, thid) :
		"显示单个帖子"
		dict_render = UserAgentSnap.record(request)
		try :
			thid = int(thid)
		except ValueError :
			raise Http404()
		group_qry = ForumSnapOld.group_find_by_sname(sname)
		if not group_qry :
			raise Http404()
		qry = ForumSnapOld.thread_find_by_thid(thid, group_qry.id)
		if not qry :
			raise Http404()
		if not ForumSnapOld.view_verify('thread', request, thid, group_qry.id) :
			raise Http403('您没有权限查看本页面')
		dict_render['group_data'] = group_qry
		dict_render['thread_data'] = qry
		attach_list = ForumSnapOld.attach_wrap(qry.attach_uuid)
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
		}
		# 计算 response_list: 根据回复排序
		response_qry = ForumSnapOld.response_find_by_thid(thid)
		if request.GET.get('dependence') == 'true' :
			def fetch_thread(level, src, aid) :
				'将 response_list 中回复 src, aid 的条目采集出，然后递归'
				for i in response_list[:] :
					if level > recursive_limit :
						break
					if i.reply_relation != src or i.reply_id != aid :
						continue
					if i not in response_list :	# should not happen
						logger.error('Error in fetch_thread. Thid = %d' % thid)
					response_sorted.append((level, i))
					response_list.remove(i)
					fetch_thread(level + 1, 'response', i.id)
			
			response_sorted = []
			response_list = list(response_qry)
			recursive_limit = len(response_list)
			fetch_thread(1, 'thread', thid)
			dict_render['dependence'] = True
		else :
			try :
				rid = int(request.GET.get('response', '0'))
				i = list(response_qry.values_list('id', flat=True)).index(rid)
				index = i // 10 + 1
			except ValueError :
				index = None
			response_sorted = zip(itertools.repeat(0.5), AuthDicts.page_dict \
							(request, response_qry, 10, dict_render, index))
		dict_render['response_list'] = [dict_thread]	# 第一个渲染帖子本身的内容
		children_dict = {}								# 用指针的作用，以提高效率
		for level, i in response_sorted :
			# 附件
			attach_list = ForumSnapOld.attach_wrap(i.attach_uuid)
			# 子回复
			children_list = []
			for j in response_qry.filter(reply_relation='response', 
								reply_id=i.id).values_list('id', flat=True) :
				if j not in children_dict :
					children_dict[j] = {}
				children_list.append(children_dict[j])
			# 父回复
			if i.reply_relation == 'response' :
				if i.reply_id not in children_dict :
					children_dict[i.reply_id] = {}
				father = children_dict[i.reply_id]
			else :
				father = ''
			# 添加到 dict_render
			dict_render['response_list'].append({
				'data': i, 
				'relation': 'response', 
				'level': level, 
				'time_create': ChineseSnap.datetime_simp(i.time_create), 
				'avatar': AvatarSnap.avatar_all(i.send_relation, i.send_id), 
				'nickname': UserSnap.nickname_find_by_uid(i.send_id), 
				'sname': UserSnap.sname_find_by_uid(i.send_id), 
				'attach': attach_list, 
				'attach_len': len(attach_list), 
				'attach_uuid': i.attach_uuid, 
				'father': father, 
				'children_list': children_list, 
			})
		from quan_news.views import NewsSnap
		remove_space = lambda x: re.sub('\s+', ' ', x).strip()
		for i in response_qry.filter(id__in=children_dict) :		# 补全信息
			extract_limit = 50
			extracted = remove_space \
								(' '.join(NewsSnap.content_extract(i.content)))
			if len(extracted) > extract_limit :
				extracted = extracted[:extract_limit] + ' ...'
			children_dict[i.id].update({
				'data': i, 
				'nickname': UserSnap.nickname_find_by_uid(i.send_id), 
				'sname': UserSnap.sname_find_by_uid(i.send_id), 
				'extracted': extracted, 
			})
		dict_render.update(ForumSnapOld.thread_latest_render())
		dict_render['title'] = t_(' - %s') % qry.subject
		return Snap.render('forum_old_thread.html', dict_render)

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
		reply_src = request.POST.get('reply_src')
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
				group_qry = ForumSnapOld.group_find_by_sname(sname)
				if not group_qry :
					raise Http404('找不到群组')
				thid, gid = None, group_qry.id
				subject_required = True
				dict_render['page_title'] = '发表帖子'
			elif relation == 'response' :
				if reply_src == 'thread' :
					thid = reply_aid
				elif reply_src == 'response' :
					rid = reply_aid
					thid = ForumSnapOld.thid_find_by_rid(rid)
				else :
					raise Http404('参数错误')
				gid = ForumSnapOld.gid_find_by_thid(thid)
				if not gid or not thid :
					raise Http404('参数错误')
				group_qry = ForumSnapOld.group_find_by_gid(gid)
				subject_required = False
				dict_render['page_title'] = '发表回复'
			else :
				raise Http404('参数错误')
			if not ForumSnapOld.creator_verify(relation, request, thid, gid) :
				raise Snap.error('您没有权限')
			qry = None
		elif action == 'edit' :
			if relation == 'group' :
				qry = ForumSnapOld.group_find_by_sname(sname)
				subject_required = True
				aid = qry.id
				dict_render['page_title'] = '编辑板块信息'
				dict_render['data_account_sname'] = UserSnap.sname_find_by_uid \
																(qry.account_id)
			elif relation == 'thread' :
				qry = ForumSnapOld.thread_find_by_thid(aid)
				subject_required = True
				dict_render['page_title'] = '编辑帖子'
			elif relation == 'response' :
				qry = ForumSnapOld.response_find_by_rid(aid)
				subject_required = False
				dict_render['page_title'] = '编辑回复'
			else :
				raise Http404('参数错误')
			if not qry :
				raise Http404('找不到对象')
			if not ForumSnapOld.edit_verify(relation, request, qry) :
				if relation == 'group' and \
					ForumSnapOld.forum_admin_verify(request) :
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
			dict_render['reply_src'] = reply_src
			dict_render['aid'] = aid
			dict_render['data'] = qry
			dict_render['subject_required'] = subject_required
			dict_render['replied'] = ForumSnapOld.replied(relation, aid)
			group_qry = ForumSnapOld.group_find_by_sname(sname)
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
				dict_render['attach_allowed'] = True
			dict_render.update(ForumSnapOld.thread_latest_render())
			dict_render['title'] = ' - 创建或编辑对象'
			return Snap.render('forum_old_post.html', dict_render)
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
				qry = ForumGroupOld(relation='user', subject=subject, 
								content=content)
			elif relation == 'thread' :
				qry = ForumThreadOld(send_id=request.user.id, 
								send_relation='user', subject=subject, 
								content=content, group_id=gid)
			else :	# relation == 'response'
				qry = ForumResponseOld(send_id=request.user.id, 
								send_relation='user', reply_id=reply_aid, 
								reply_relation=reply_src, content=content, 
								thread_id=thid)
		else :	# action == 'edit'
			if relation == 'group' :
				history = ForumHistoryOld(relation='group', account_id=qry.id, 
									subject=qry.subject, content=qry.content)
				qry.subject = subject
				qry.content = content
			elif relation == 'thread' :
				history = ForumHistoryOld(relation='thread', account_id=qry.id, 
									subject=qry.subject, content=qry.content)
				qry.subject = subject
				qry.content = content
			else :	# relation == 'response'
				history = ForumHistoryOld(relation='response', account_id=qry.id, 
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
				ForumSnapOld.sname_validate(simp_name)
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
			thread = ForumSnapOld.thread_find_by_thid(thid)
			if thread :
				thread.response_number += 1
				thread.save()
		# 返回消息
		if relation == 'group' :
			url = '/forum-old/%s/' % qry.simp_name
			if action == 'new' :
				comment = '成功创建板块'
			else :
				comment = '成功编辑板块信息'
		elif relation == 'thread' :
			url = '/forum-old/%s/%d/' % (sname, qry.id)
			if action == 'new' :
				comment = '发帖成功'
			else :
				comment = '成功编辑帖子'
		else :	# relation == 'response'
			url = '/forum-old/%s/%d?response=%d#response-%d' % \
								(sname, qry.thread_id, qry.id, qry.id)
			if action == 'new' :
				comment = '回复成功'
			else :
				comment = '成功编辑回复'
		return Snap.success(request, comment, { 'redirect': url })

	@vary_on_cookie
	def forum_delete(request, sname) :
		'删除论坛的内容'
		dict_render = UserAgentSnap.record(request)
		if request.method != 'POST' :
			return Snap.redirect('/forum-old/%s/' % sname)
		relation = request.POST.get('relation')
		aid = request.POST.get('aid')
		if not relation or not aid :
			raise Snap.error('参数不完整')
		ForumSnapOld.delete(relation, aid)
		return Snap.success(request, '删除成功', { 'redirect': '/forum-old/' })

	@vary_on_cookie
	def random(request, *arguments) :
		dict_render = UserAgentSnap.record(request)
		thread_qry = ForumSnapOld.public_thread_list()
		thread_number = thread_qry.count()
		if not thread_number :
			return Snap.redirect('/forum-old/')
		index = random.randrange(thread_number)
		return Snap.redirect(ForumSnapOld.url_find_by_thread(thread_qry[index]))


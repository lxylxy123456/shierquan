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

from quan_account.views import *
from quan_avatar.views import AvatarSnap
from quan_message.views import MessageSnap
from quan_message.views import PublicMessageAction, PrivateMessageAction
from quan_ua.views import *

class EventSnap:
	def event_signup(evid, uid, answer, manual=False) :
		'判断先前签到次数并签到，manual=True代表自动通过'
		rqy = EventRelation.objects.filter(event_id=evid, account_id=uid, 
						relation='signup')
		if rqy.exists() :
			return None # 已经签到
		try :
			quest = EventQuest.objects.get(event_id=evid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None	# 没有设置签到
		if quest.answer == answer or manual :
			qry = EventRelation(event_id=evid, account_id=uid, 
					relation='signup', status='success')
		else :
			qry = EventRelation(event_id=evid, account_id=uid, 
					relation='signup', status='failure')
		qry.save()
		return qry

	def event_find_by_evid(evid) :
		'通过evid寻找事件'
		try :
			return EventInfo.objects.get(category__in=('history', ''), 
											id=evid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def event_find_by_uid(uid) :
		'用户签到成功的活动'
		target = EventRelation.objects.filter(account_id=uid, status='success',
						relation='signup').values_list('event_id', flat=True)
		return EventInfo.objects.filter(id__in=target).order_by('-time_set')

	def event_find_by_cid(src, aid, history=True) :
		'通过账户ID获取所有活动'
		if history :
			return EventInfo.objects.filter(account_id=aid, relation=src, 
											category__in=('history', ''))
		else :
			return EventInfo.objects.filter(account_id=aid, relation=src, 
											category='')

	def event_month_find_by_cid(src, aid) :
		'得到一个月前的所有活动'
		cache_key = 'EventSnap__event_month_find_by_cid__%s_%d' % (src, aid)
		cached = cache.get(cache_key)
		if cached != None :
			return cached
		d = datetime.now() - timedelta(30)
		qry = EventInfo.objects.filter(account_id=aid, relation=src, 
								category__in=('history', ''), time_end__gte=d)
		cache.set(cache_key, qry, 86400)
		return qry

	def semester_start(now=None) :
		'得到学期开始时间，默认为3月和9月开学'
		now = now or datetime.now()
		month_start = (3, 9)									# 开始的月份，1日
		for i in reversed(sorted(month_start)) :				# 从后往前匹配
			if i <= now.month :
				return datetime(now.year, i, 1)
		return datetime(now.year - 1, semester_start[-1], 1)	# 无匹配表示前一年

	def event_semester_find_by_cid(src, aid) :
		'得到一个学期的所有活动'
		cache_key = 'EventSnap__event_semester_find_by_cid__%s_%d' % (src, aid)
		cached = cache.get(cache_key)
		if cached != None :
			return cached
		qry = EventInfo.objects.filter(account_id=aid, relation=src, 
									category__in=('history', ''), 
									time_end__gte=EventSnap.semester_start())
		cache.set(cache_key, qry, 86400)
		return qry

	def remove(request, src, aid, evid) :
		'删除事件'
		try :
			event = EventInfo.objects.get(category__in=('history', ''), 
										account_id=aid, relation=src, id=evid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			raise Snap.error('活动不存在')
		MessageSnap.message_delete('event', evid)
		if event.category == 'history' :
			event.category = 'history-deleted'
		else :
			event.category = 'deleted'
		event.save()

	def create_frequent(src, aid, history) :
		'检测用户投递事件数量是否超标'
		qry = EventInfo.objects.filter \
				(account_id=aid, relation=src, category__in=('history', ''))
		d = datetime.now() - timedelta(0, 15, 0)
		if qry.filter(time_create__gte=d).exists() :
			raise Snap.error('投递事件太频繁')
		if not history and qry.filter(status='on').exists() :
			raise Snap.error('投递事件数量超标') # 有接下来的活动，不能投递新的非历史活动

	def event_next_find_by_cid(src, aid) :
		'获取接下来的活动并维护事件队列（移除旧事件）'
		qry = EventSnap.event_find_by_cid(src, aid, False).filter(status='on')
		answer = None
		for event in qry :
			if EventSnap.time_status(event) == 1 :		# 活动已经结束
				event.status = 'off'	
				event.save()
			else :										# 是否是最近的一次活动
				if not answer or event.time_create < answer.time_create :
					answer = event
		return answer

	def follower_create(evid, uid) :
		'添加关注者'
		eqy = EventSnap.event_find_by_evid(evid)
		oqy = EventRelation.objects.filter(account_id=uid, event_id=evid, 
			relation='follower')
		if not eqy or oqy.exists() :
			return None
		cqy = EventRelation(account_id=uid, event_id=evid, relation='follower')
		cqy.save()
		return cqy

	def follower_total(evid) :
		'获取关注者数量'
		return EventRelation.objects.filter \
					(event_id=evid, relation='follower').count()

	def nice_create(evid, uid) :
		'新增赞'
		eqy = EventSnap.event_find_by_evid(evid)
		oqy = EventRelation.objects.filter(event_id=evid, account_id=uid,
				relation="nice")
		if not eqy or oqy.exists() :
			return None
		nqy = EventRelation(event_id=evid, account_id=uid, relation="nice")
		nqy.save()
		return nqy

	def nice_total(evid) :
		'赞总数'
		return EventRelation.objects.filter \
					(event_id=evid, relation="nice").count()

	def signup_total(evid) :
		'签到了的用户总数'
		return EventRelation.objects.filter \
				(relation='signup', status='success', event_id=evid).count()

	def time_convert(time_str) :
		'时间字符串 => 时间结构'
		return datetime.strptime(time_str, "%Y/%m/%d %H:%M")

	def event_filter_by_request(request) :
		'获取用户所属社团的有效活动'
		cid_list = ClubSnap.club_find_by_uid(request.user.id, True, False)
		ev_set = EventInfo.objects.filter(category__in=('history', ''), 
			relation='club', account_id__in=cid_list, status='on')
		return ev_set.order_by("-time_set")

	def quest_set_by_evid(evid) :
		'检测是否为事件设置签到'
		return EventQuest.objects.filter(event_id=evid).exists()
		
	def quest_find_by_evid(evid) :
		'获取提问'
		try :
			return EventQuest.objects.get(event_id=evid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def signed_get_by_event(event) :
		from quan_auth.views import AuthSnap
		'得到已经签到的人员列表（event为数据库行）'
		event_dict = {}
		sign_qry = EventRelation.objects.filter(event_id=event.id, 
			relation='signup')
		event_dict['participator'] = sign_qry.count()
		event_dict['club_member'] = []
		cid = event.account_id
		for single_sign in sign_qry :
			if single_sign.status == 'failure':
				status = t_('失败')
			else:
				status = t_('成功')
			grade_num = UserSnap.grade_find_by_uid(single_sign.account_id, True)
			uid = single_sign.account_id
			rank = AuthSnap.mrank_calc(uid, cid)
			part = AuthSnap.ratio_join(uid, cid)
			event_dict['club_member'].append({
				'name': UserSnap.fname_find_by_uid(single_sign.account_id),
				'grade': grade_num,
				'rank': int(rank),
				'participate': str(int(part*1000)/10)+'%',
				'status': status, 
				'status_en': single_sign.status, 
			})
		event_dict['club_member_number'] = len(sign_qry)
		return event_dict

	def signed_find_by_uid(evid, uid) :
		'uid 是否为 evid 签过到'
		return EventRelation.objects.filter \
				(event_id=evid, relation='signup', account_id=uid).exists()

	def follower_find_by_evid(evid) :
		'得到关注者列表'
		follower_list = []
		for i in EventRelation.objects.filter \
				(event_id=evid, relation='follower').order_by('-time_create') :
			grade_num = UserSnap.grade_find_by_uid(i.account_id)
			follower_list.append({
				'name': UserSnap.fname_find_by_uid(i.account_id),
				'follow_time': ''.join(ChineseSnap.datetime_simp(i.time_create)), 
			})
		return follower_list

	def event_attendence_by_uid(uid, cid, month=False) :
		'获取社员参与活动总时间和社团活动总时间'
		time_total = timedelta(0)
		if month :
			qry = EventSnap.event_month_find_by_cid('club', cid)
		else :
			qry = EventSnap.event_semester_find_by_cid('club', cid)
		user_record = timedelta(0)
		club_record = timedelta(0)
		success = EventRelation.objects.filter(account_id=uid, status='success',
						relation='signup').values_list('event_id', flat=True)
		for event in qry.iterator() :
			event_time = event.time_end - event.time_set
			club_record += event_time
			if event.id in success :
				user_record += event_time
		return user_record, club_record

	def time_status(event) :
		'表示活动的时间情况，完成为1，未开始为-1，正在进行为0'
		now = datetime.now()
		if now < event.time_set :
			return -1
		elif now > event.time_end + timedelta(0, 3600, 0) :
			return 1
		else :
			return 0

	def niced_find_by_request(request, evid) :
		'是否已经赞'
		return EventRelation.objects.filter(event_id=evid, relation="nice", 
				account_id=UserSnap.uid_find_by_request(request)).exists()

	def followed_find_by_request(request, evid) :
		'是否已经跟随'
		return EventRelation.objects.filter(event_id=evid, relation="follower", 
				account_id=UserSnap.uid_find_by_request(request)).exists()

	def history_check(time_set, time_end) :
		'在创建活动时判断时间是否可行（20分钟前以后），返回是否是历史活动'
		if time_set < datetime.now() - timedelta(1200) :
			return True
		elif time_end < datetime.now() :
			return True
		else :
			return False

	def event_search(query) :
		return EventInfo.objects.filter(Q(subject__icontains=query) | 
										Q(content__icontains=query) | 
										Q(location__icontains=query), 
										category__in=('history', ''))

	def join_find(evid, success=False) :
		'返回qry'
		qry = EventRelation.objects.filter(event_id=evid, relation='signup')
		if success :
			return qry.filter(status='success')
		else :
			return qry

	def signup_qrcode_find_by_evid(evid) :
		try :
			qry = EventQuest.objects.get(event_id=evid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None
		token = qry.token
		if not token :
			return None
		return '/media/images/qrcode/signup-%d-%d.png' % (evid, token)

	def signup_qrcode_create(evid) :
		try :
			qry = EventQuest.objects.get(event_id=evid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return False
		if qry.token != 0 :	# 已经生成
			return False
		token = 0
		while not token :
			token = datetime.now().microsecond
		name = 'signup-%d-%d.png' % (evid, token)
		templ = 'http://shierquan.tk/event/signup/qrcode/?evid=%d&token=%d'
		content = templ % (evid, token)
		path = os.path.join(settings.MEDIA_ROOT, 'images', 'qrcode', name)
		qrcode.make(content).save(path)
		qry.token = token
		qry.save()
		return True

	def signup_qrcode_check(evid, token) :
		'token不一定是int'
		try :
			token = int(token)
		except ValueError :
			return False
		qry = EventQuest.objects.filter(event_id=evid)
		if qry :
			if qry[0].token == token :
				return True
		return False

class EventDicts :
	def club_admin(club, base_dict):
		'社团活动模块管理界面'
		dict_event = {}
		dict_event['inc_event'] = 'club/prv_event.html'
		dict_event['modal_target'] = '#event_add_box'
		dict_event['modal_content'] = '添加活动'
		dict_event['modal_info'] = '添加一个活动'
		dict_event['inc_list'] = base_dict['inc_list']
		dict_event['inc_list'].append({'name': 'club_prv_event',})
		nev = EventSnap.event_next_find_by_cid('club', club.id)
		print(nev)
		#ev_list
		ev_list = []
		event_list = EventSnap.event_find_by_cid \
			('club', club.id).order_by('-time_set')[0:8]
		for i in event_list:
			date_time = ChineseSnap.datetime_simp(i.time_set)
			date_str = date_time[0][:-1]
			time_str = date_time[1]
			ev_list.append({'data': i,'date': date_str, 'time': time_str})
		dict_event['ev_list'] = ev_list
		if nev is None :
			return dict_event
		else :
			time_set = nev.time_set
			time_end = nev.time_end
			dict_event['event'] = nev
		print(time_set, time_end)
		if time_set < datetime.now() < time_end + timedelta(0, 3600, 0):
			# 添加/当前进行的签到
			if EventSnap.quest_set_by_evid(nev.id):
				print('il:',dict_event['inc_list'])
				dict_event['event'] = EventSnap.signed_get_by_event(nev)
				dict_event['event']['id'] = nev.id
				dict_event['inc_event'] = "club/prv_signup_status.html"
				dict_event['modal_target'] = '#event_signup_status_box'
				dict_event['modal_content'] = '签到状况'
				dict_event['modal_info'] = '查看成员是否签到'
			else:
				dict_event['inc_list'].append({'name': 'club_prv_signup',})
				dict_event['inc_event'] = "club/prv_signup.html"
		else :
			# 下一次活动
			dict_event['inc_event'] = "club/shr_next_event.html"
			date, time = ChineseSnap.datetime_comp(time_set)
			dict_event['event_date'] = date
			dict_event['event_time'] = time
			dict_event['ev_list'] = ev_list[1:]
		return dict_event

	def club(request, club):
		'社团活动模块用户界面'
		nev = EventSnap.event_next_find_by_cid('club', club.id)
		dict_event = {}
		uid = UserSnap.uid_find_by_request(request)
		#ev_list
		ev_list = []
		event_list = EventSnap.event_find_by_cid \
			('club', club.id).order_by('-time_set')[0:8]
		for i in event_list:
			date_time = ChineseSnap.datetime_comp(i.time_set)
			date_str = date_time[0][0:-4]	# 可能不稳定
			time_str = date_time[1]
			ev_list.append({'data': i,'date': date_str, 'time': time_str})
		if nev is None :
			dict_event['inc_event'] = "club/pub_event.html"
			if ev_list :
				dict_event['ev_list'] = ev_list[1:]
				dict_event['event'] = ev_list[0]
				event = ev_list[0]['data']
				dict_event['nice_total'] = EventSnap.nice_total(event.id)
				dict_event['follower_total'] = EventSnap.follower_total(event.id)
				dict_event['niced'] = EventSnap.niced_find_by_request(request, event.id)
				dict_event['event_followed'] = EventSnap.followed_find_by_request(request, event.id)
			return dict_event
		else :
			time_set = nev.time_set
			time_end = nev.time_end
			date_time = ChineseSnap.datetime_comp(nev.time_set)
			date_str = date_time[0][0:-4]
			time_str = date_time[1]
			dict_event['event'] = {'data': nev,'date': date_str, 'time': time_str}
			dict_event['ev_list'] = ev_list[1:]

		follower_num = EventSnap.follower_total(nev.id)
		if time_set < datetime.now() < time_end + timedelta(0, 3600, 0):
			# 签到 
			dict_event['signed_set'] = EventSnap.signed_find_by_uid(nev.id, uid)
			dict_event['inc_event'] = "club/pub_signup.html"
			dict_event['question'] = EventSnap.quest_find_by_evid(nev.id)
		else :
			# 下一次活动
			dict_event['event_next'] = True
			#dict_event['inc_event'] = "club/shr_next_event.html"
			dict_event['inc_event'] = "club/pub_event.html"
			#date, time = ChineseSnap.datetime_comp(time_set)
			#dict_event['event_date'] = date
			#dict_event['event_time'] = time
			dict_event['nice_total'] = EventSnap.nice_total(nev.id)
			dict_event['follower_total'] = EventSnap.follower_total(nev.id)
			dict_event['niced'] = EventSnap.niced_find_by_request(request, nev.id)
			dict_event['event_followed'] = EventSnap.followed_find_by_request(request, nev.id)
		return dict_event
		
	def single_event(request, evid) :
		event = EventSnap.event_find_by_evid(evid)
		if not event :
			return None
		evid = int(evid)
		event_dict = {'data':event,}
		date_string, time_end = ChineseSnap.datetime_comp(event.time_end)
		date_string, time_string = ChineseSnap.datetime_comp(event.time_set)
		event_dict['content'] = event.content.split('\n')
		event_dict['day_set'] = date_string
		event_dict['time_set'] = time_string
		event_dict['time_end'] = time_end
		event_dict['avatar'] = AvatarSnap.avatar_find(event.relation, event.account_id)
		event_dict['follower'] = EventSnap.follower_total(evid)
		event_dict['nice'] = EventSnap.nice_total(evid)
		event_dict['niced'] = EventSnap.niced_find_by_request(request, evid)
		event_dict['event_followed'] = EventSnap.followed_find_by_request(request, evid)
		if event.relation=='user':
			event_dict['sponsor_fname'] = '用户' + str(event.account_id)
		else:
			event_dict['sponsor_fname'] = ClubSnap.fname_find_by_cid \
															(event.account_id)
		event_dict['sponsor_sname'] = AccountSnap.sname_find_by_aid(event.relation, event.account_id)
		president = ClubSnap.cid_verify(request, event.account_id, True)
		event_dict.update(EventSnap.signed_get_by_event(event))
		event_dict['follower_list'] = EventSnap.follower_find_by_evid(event.id)
		event_dict['quest'] = EventSnap.quest_find_by_evid(event.id)
		time_status = EventSnap.time_status(event)

		# 计算需要显示的模块
		event_dict['president'] = president
		show = ()
		if president :
			if time_status == 0 and not event_dict['quest'] :
				show = ('signup_set', )
			elif time_status != -1 :
				show = ('join', 'signup_manual')
				if time_status == 0 :
					event_dict['signup_qrcode'] = \
									EventSnap.signup_qrcode_find_by_evid(evid)
		else :
			uid = UserSnap.uid_find_by_request(request)
			if time_status == 0 and event_dict['quest'] :
				if uid and not EventSnap.signed_find_by_uid(evid, uid) :
					show = ('signup', )
		for i in show :
			event_dict['show_%s' % i] = True
		
		# 为 share 和 event 关联渲染
		from quan_share.views import ShareSnap
		event_dict['share_list'] = [[]]
		event_dict['related_list'] = []
		related_list = []
		for i in ShareEventRelation.objects.filter(event_id=evid, status=0) :
			related_list.append(i.share_id)
		club_avatar = AvatarSnap.avatar_find \
			(event.relation, event.account_id, 'large')
		for i in ShareSnap.share_find_by_aid(event.relation, event.account_id) :
			thumbnail = ''
			if i.id in related_list :
				event_dict['relate_exist'] = True
				thumbnail = ShareSnap.thumbnail_find(i.attach_uuid, 'large')
			if not thumbnail :
				thumbnail = club_avatar
			append_object = {
				'data': i, 
				'related': i.id in related_list, 
				'date': ChineseSnap.datetime_simp(i.time_create), 
				'thumbnail': thumbnail, 
				'content': i.content.split('\n'), 
			}
			if len(event_dict['share_list'][-1]) < 10 :
				event_dict['share_list'][-1].append(append_object)
			else :
				event_dict['share_list'].append([append_object])
		return event_dict

class EventViews:
	@vary_on_cookie
	@UserAuthority.logged_in
	def event_signup_submit(request):
		'社员签到'
		dict_render = UserAgentSnap.record(request)
		if request.method != 'POST' :
			raise Http403('方法错误')
		try :
			evid = int(request.POST.get('evid', ''))
		except ValueError :
			raise Snap.error('找不到活动')
		answer = request.POST.get('choice', '')
		uid = UserSnap.uid_find_by_request(request)
		event = EventSnap.event_find_by_evid(evid)
		if not event :
			raise Snap.error('找不到活动')
		status = EventSnap.event_signup(event.id, uid, answer)
		if status and status.status != 'failure' :
			PublicMessageAction.save(request, 'signup', 'success',
			 						uid, 'user', evid, 'event')
			PrivateMessageAction.save('您已经签到成功', evid, 
				'event-signup', uid, 'user', event.account_id, 'club')
			return Snap.success(request, '活动签到成功')
		else :
			PrivateMessageAction.save('您已经签到失败', evid, 
				'event-signup', uid, 'user', event.account_id, 'club')
			raise Snap.error('活动签到失败')

	@vary_on_cookie
	@UserAuthority.logged_in
	def event_signup_qrcode(request) :
		dict_render = UserAgentSnap.record(request)
		try :
			evid = int(request.GET.get('evid', ''))
		except ValueError :
			raise Http404('活动不合法')
		uid = UserSnap.uid_find_by_request(request)
		token = request.GET.get('token', '')
		if EventSnap.signup_qrcode_check(evid, token) :
			EventSnap.event_signup(evid, uid, '', True)
			PublicMessageAction.save(request, 'signup', 'success', 
									uid, 'user', evid, 'event')
			return Snap.redirect('/event/%d/?status=success' % evid)
			
		else :
			return Snap.redirect('/event/%d/?status=warning' % evid)

	@vary_on_cookie
	@UserAuthority.logged_in
	def event_signup_create(request):
		'创建签到'
		dict_render = UserAgentSnap.record(request)
		if request.method != 'POST' :
			raise Http404('方法错误')
		json_dict = json.loads(request.POST.get('data', ''))
		src = request.POST.get('src', '')
		aid = int(request.POST.get('aid', -1))
		event = EventSnap.event_next_find_by_cid(src, aid)
		if event == None :
			raise Http404('没有找到这个活动，似乎过期了？')
		UserAuthority.assert_permission(request, src, aid, True)
		eform = EventQuestForm(json_dict)
		if not eform.is_valid():
			raise Snap.error('请检查输入是否存在空白或超出长度限制')
		else :
			einst = eform.save(commit=False)
			einst.event_id = event.id
			einst.save()
			fname = AccountSnap.fname_find_by_aid(event.relation, 
												event.account_id)
			PublicMessageAction.save(request, 'signup', 'new', aid, 
									src, event.id, 'event')
			EventSnap.signup_qrcode_create(event.id)
			return Snap.success(request, '成功创建签到', 
								{ 'redirect': '/event/%d/' % event.id })

	@vary_on_cookie
	@UserAuthority.logged_in
	def event_create(request, history=False):
		'创建新活动'
		dict_render = UserAgentSnap.record(request)
		if request.method == 'POST':
			try :
				json_dict = json.loads(request.POST.get('data', ''))
			except json.JSONDecodeError :
				raise Snap.error('表单不完整，可向HCC汇报此错误')
			src = request.POST.get('src', '')
			aid = int(request.POST.get('aid', -1))
			UserAuthority.assert_permission(request, src, aid, True)
			EventSnap.create_frequent(src, aid, history)
			eform = EventInfoForm(json_dict)
			content = json_dict.get('content', '')
			if not eform.is_valid() or (not content and not history) :
				raise Snap.error('输入内容不完整或字数过多')
			else :
				einst = eform.save(commit=False)
				einst.content = content
				try :
					time_set = json_dict.get('time_set', '')
					einst.time_set = EventSnap.time_convert(time_set)
					if history :
						einst.time_end = einst.time_set + timedelta(0, 3600, 0)
						einst.content = '%s历史活动 - %s' % \
							(AccountSnap.fname_find_by_aid(src, aid), einst.subject)
					else :
						time_end = json_dict.get('time_end', '')
						einst.time_end = EventSnap.time_convert(time_end)
				except ValueError :
					raise Snap.error('时间信息不完整')
				einst.account_id = aid
				einst.relation = src
				if einst.time_set > einst.time_end :
					raise Snap.error('开始时间>结束时间？')
				if EventSnap.history_check(einst.time_set, einst.time_end) :
					history = True
				if history :
					einst.status = 'off'
					einst.category = 'history'
				else :
					einst.status = 'on'
				if history and einst.time_end > datetime.now() :
					raise Snap.error('您输入的内容不合法。')
				try :
					einst.save()
				except DataError :
					raise Snap.error('或许信息太长了？')
				QrcodeSnap.qrcode_create(einst.id, 'event')
				if 1 or not history :
					PublicMessageAction.save(request, 'event', 'new', aid, 
						src, einst.id, 'event')
					PrivateMessageAction.save('新活动 - %s' % einst.subject, 
						einst.id, 'event', aid, src, aid, src)
					PrivateMessageAction.follower_send \
						(aid, '%s创建了新活动' % ClubSnap.fname_find_by_cid(aid), 
						einst.id, 'event')
				CacheSnap.event_created(src, aid, einst.id)
				return Snap.success(request, '活动已成功提交', { 'reload': True })
		else:
			raise Http404()

	@vary_on_cookie
	@UserAuthority.logged_in
	def event_cancel(request):
		'取消活动'
		dict_render = UserAgentSnap.record(request)
		if request.method != 'POST':
			raise Http404()
		src = request.POST.get('src', '')
		aid = int(request.POST.get('aid', -1))
		evid = int(request.POST.get('evid', -1))
		UserAuthority.assert_permission(request, src, aid, True)
		EventSnap.remove(request, src, aid, evid)
		url = '/club/%s/' % AccountSnap.sname_find_by_aid(src, aid)
		CacheSnap.event_canceled(src, aid, evid)
		return Snap.success(request, '已成功移除活动', { 'redirect': url })

	@vary_on_cookie
	def event_show(request, evid):
		"显示活动页面"
		dict_render = UserAgentSnap.record(request)
		event = EventDicts.single_event(request, evid)
		if not event :
			raise Http404('找不到活动')
		dict_render['event'] = event
		dict_render['title'] = t_(' - %s - %s的活动') % (event['data'].subject, 
				event['sponsor_fname'])
		dict_render['visitors'] = AccountSnap.visit_count_by_account \
															(event['data'])
		dict_render['signup_status'] = request.GET.get('status', '')
		dict_render['title'] = t_(' - %s') % event['data'].subject
		return Snap.render('event_view.html', dict_render)

	@vary_on_cookie
	@UserAuthority.logged_in
	def event_manual(request, evid):
		'活动补签页面'
		dict_render = UserAgentSnap.record(request)
		event = EventSnap.event_find_by_evid(evid)
		if not event or not ClubSnap.cid_verify(request, event.account_id, True):
			raise Http403('您没有活动的管理权限')
		fname = request.POST.get('fname', '')
		uid = UserSnap.uid_find_by_fname(fname)
		if uid == None :
			raise Snap.error('找不到用户')
		if EventSnap.quest_find_by_evid(evid) == None :
			raise Snap.error('没有设置签到')
		if EventSnap.event_signup(evid, uid, '', True) :
			return Snap.success(request, t_('成功为%s补签，请刷新页面') % fname)
		else :
			raise Snap.error('已经签到')

	@vary_on_cookie
	@UserAuthority.logged_in
	def event_nice(request):
		'[JSON] 用户赞事件 返回赞总数'
		dict_render = UserAgentSnap.record(request)
		if request.method != 'POST':
			raise Http404()
		uid = UserSnap.uid_find_by_request(request)
		evid = int(request.POST.get('evid', -1))
		if not EventSnap.nice_create(evid, uid) :
			raise Snap.error('您已经赞过这个活动')
		ufname = UserSnap.fname_find_by_request(request)
		event = EventSnap.event_find_by_evid(evid)
		cfname = AccountSnap.fname_find_by_aid(event.relation, event.account_id)
		PublicMessageAction.save(request, 'event', 'nice', 
			UserSnap.uid_find_by_request(request), 'user', evid, 'event')
		return Snap.success(request, '成功为活动点赞', 
							{ 'nice_total': EventSnap.nice_total(evid) })

	@vary_on_cookie
	@UserAuthority.logged_in
	def event_follow(request):
		'[JSON] 用户跟随事件 返回跟随总数'
		dict_render = UserAgentSnap.record(request)
		if request.method != 'POST':
			raise Http404()
		resp_data = {}
		uid = UserSnap.uid_find_by_request(request)
		evid = int(request.POST.get('evid', -1))
		event = EventSnap.event_find_by_evid(evid)
		if event == None :
			raise Snap.error('您没有权限')
		aid = event.account_id
		if event.time_set > datetime.now() :
			status = EventSnap.follower_create(evid=evid, uid=uid)
			action = 'follow'
		else :
			status = EventSnap.nice_create(evid=evid, uid=uid)
			action = 'nice'
		if status != None :
			PublicMessageAction.save(request, 'event', action, uid, 'user', 
										evid, 'event')
		return Snap.success(request, '关注成功', 
						{ 'follower_total': EventSnap.follower_total(evid) })

	@vary_on_cookie
	def event_latest(request, record=True) :
		if record :
			dict_render = UserAgentSnap.record(request)
		qry = EventInfo.objects.filter(category__in=('history', ''))
		try :
			evid = qry.order_by('-time_create')[0].id
			return Snap.redirect("/event/%d/" % evid)
		except IndexError :
			raise Http404('十二圈中似乎还没有活动')

	@vary_on_cookie
	def event_next(request) :
		dict_render = UserAgentSnap.record(request)
		qry = EventInfo.objects.filter \
			(category__in=('history', ''), time_set__gte=datetime.now())
		try :
			evid = qry.order_by('time_set')[0].id
			return Snap.redirect("/event/%d/" % evid)
		except IndexError :
			return EventViews.event_latest(request, False)

	def event_share_relate(request, evid) :
		'关联 event 和 share'
		dict_render = UserAgentSnap.record(request)
		event = EventSnap.event_find_by_evid(evid)
		if not event or not ClubSnap.cid_verify(request, event.account_id, True):
			raise Http403('您没有活动的管理权限')
		evid = int(evid)
		from quan_share.views import ShareSnap
		try :
			sid = int(request.POST.get('sid', ''))
			share = ShareSnap.share_find_by_sid(sid)
			if not share :
				raise ValueError
			if share.account_id != event.account_id :
				raise ValueError
			if share.relation != event.relation :
				raise ValueError
		except ValueError :
			raise Http403('您没有分享的管理权限')
		if request.POST.get('relate', '') == 'true' :
			ShareEventRelation(share_id=share.id, event_id=event.id).save()
			return Snap.success(request, '成功关联分享')
		else :
			ShareEventRelation.objects.filter \
					(share_id=share.id, event_id=event.id).update(status=1)
			return Snap.success(request, '成功取消分享关联')

class EventSiteMap(Sitemap) :
	def items(self) :
		return EventInfo.objects.filter(category__in=('', 'history'))
	def location(self, item) :
		return '/event/%d/' % item.id


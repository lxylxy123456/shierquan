from .models import *

from quan_event.models import EventInfo
from quan_message.models import PrivateMessage

from quan_account.views import *
from quan_auth.views import AuthSnap, AuthDicts
from quan_avatar.views import AvatarSnap
from quan_badge.views import BadgeDicts, BadgeSnap
from quan_event.views import EventDicts, EventSnap
from quan_message.views import MessageSnap
from quan_message.views import PublicMessageAction, PrivateMessageAction
from quan_share.views import ShareSnap, ShareDicts, ShareInfo
from quan_ua.views import *

class CenterDicts :
	def club_find(uid):
		'用户参与/关注的社团'
		dict_club = {}
		club_follow = ClubSnap.club_find_by_uid(uid, False)
		club_attend = ClubSnap.club_find_by_uid(uid, True)
		dict_club['follow_list'] = club_follow[:5]
		dict_club['attend_list'] = club_attend
		return dict_club

	def status(club):
		'社团状态'
		from quan_auth.views import AuthSnap
		member_sum = ClubSnap.member_total(club.id)
		active_ratio = 0
		if member_sum :
			active_sum = AuthSnap.active_total(club.id)
			if active_sum :
				active_ratio = active_sum / member_sum
		dict_status = {
			'club_watch_num':	ClubSnap.follower_total(club.id), 
			'club_member_num':	ClubSnap.member_total(club.id), 
			'club_follower_num':ClubSnap.follower_total(club.id), 
			'club_event_num':	EventSnap.event_find_by_cid \
											('club', club.id, True).count(), 
			'club_attendance':	"%.2f" % (active_ratio * 100), 
			'club_badge_num':	BadgeSnap.badge_total_by_cid('club', club.id), 
			'club_wait_num':	ClubSnap.member_wait_find(club.id).count()
		}
		head_user = ClubSnap.head_find_by_cid(club.id)
		vice_user = ClubSnap.vice_find_by_cid(club.id)
		if head_user :
			dict_status.update({
				'club_head':		head_user.first_name, 
				'club_head_sname':	head_user.last_name, 
			})
		if vice_user :
			dict_status.update({
				'club_vice':		vice_user.first_name, 
				'club_vice_sname':	vice_user.last_name, 
			})
		return dict_status

	def club_picture(cid, request=('qrcode', 'latest', 'mixed')) :
		'得到图片板块的图片'
		dict_render = {}
		sname = ClubSnap.sname_find_by_cid(cid)
		img_qry = ShareSnap.image_list_by_aid('club', cid)
		if 'qrcode' in request :#二维码
			dict_render['qrcode'] = QrcodeSnap.qrcode_find(sname, "club")
			if len(img_qry) == 0 :
				dict_render['latest'] = None
				dict_render['mixed'] = None
				return dict_render
		if 'latest' in request :#获取最新
			dict_render['latest'] = ShareSnap.url_find_by_attach(img_qry[0])
		if 'mixed' in request :#获取杂烩
			dict_render['mixed'] = ShareSnap.mix_find(sname)
		return dict_render

	def member_manage(src, aid, render_list=('follower', 'member', 'wait')) :
		'按照render_list中的要求选择性渲染'
		if src == 'user' :
			return {}
		dict_render = {'member_wait': [], 'member': []}
		if 'wait' in render_list :	# 待审核社员
			mem_wait = ClubSnap.member_wait_find(aid)
			dict_render['member_wait_num'] = len(mem_wait)
			for i in mem_wait :
				time_create_tumple = ChineseSnap.datetime_simp(i.time_create)
				user = {
					'name': UserSnap.fname_find_by_uid(i.account_id_A), 
					'grade': UserSnap.grade_find_by_uid(i.account_id_A, True), 
					'date': time_create_tumple[0], 
					'id': i.account_id_A,
				}
				dict_render['member_wait'].append(user)
		if 'member' in render_list :	# 通过社员
			for uid in ClubSnap.member_all(aid) :
				join, total = EventSnap.event_attendence_by_uid(uid, aid)
				user = {
					'uid': uid, 
					'name': UserSnap.fname_find_by_uid(uid), 
					'grade': UserSnap.grade_find_by_uid(uid, True), 
					'ratio': '%.1f' % \
							(100.0 * (total / timedelta(1) and join / total)), 
					'score': '%.1f' % (0.2 * join / timedelta(0, 3600)), 
					'identity': ClubSnap.club_position_by_uid(aid, uid), 
					'avatar': AvatarSnap.avatar_find('user', uid, 'medium'), 
				}
				dict_render['member'].append(user)
		if 'follower' in render_list :	# 跟随者
			qry = ClubSnap.follower_find(aid)
			follower_list = []
			for i in qry :
				follower_list.append({
					'data': UserSnap.user_find_by_uid(i.account_id_A), 
					'avatar': AvatarSnap.avatar_find('user', i.account_id_A, 
								size="medium"),
				})
			dict_render['follower_list'] = follower_list
		return dict_render

	def detail(src, qry, category) :
		'category in (sent, inbox, follow, event, share)'
		detail_list = []
		if category == 'share' :
			for i in qry :
				date_time = ChineseSnap.datetime_simp(i.time_create)
				detail_list.append({
					'link': '/share/%s/' % i.attach_uuid, 
					'date': date_time[0], 
					'data': i, 
					'time': date_time[1], 
				})
		elif category == 'event' :
			for i in qry :
				date_time = ChineseSnap.datetime_simp(i.time_set)
				detail_list.append({
					'link': '/event/%s/' % i.id, 
					'date': date_time[0], 
					'data': i, 
					'time': date_time[1], 
				})
		else :
			# There is an error, l gave up fixing it in 201510172138
			for i in qry :
#				link = MessageSnap.link_find(i, category)
#				if category == 'sent' :
#					con = 0 #continue
#					for j in detail_list :
#						if j['link'] == link :
#							con = 1
#							break
#					if con :
#						continue
				link = '#'		# link 的生成函数已经实效
				date_time = ChineseSnap.datetime_simp(i.time_create)
				if category == 'event' :
					event = EventSnap.event_find_by_evid(i.id)
					if event != None :
						date_time = ChineseSnap.datetime_simp(event.time_set)
				detail_list.append({
					'link': link, 
					'date': date_time[0], 
					'data': i, 
					'time': date_time[1], 
				})
		return detail_list

class CenterViews:
	@vary_on_cookie
	def club_show(request, sname):
		'显示社团主页'
		# 思考：如果增加一个_admin反而需要给社长的模板上加一个按钮去访问
		dict_render = UserAgentSnap.record(request)
		dict_render['inc_list'] = []
		real_name = ClubSnap.alias_find_by_sname(sname)
		if real_name != sname and real_name :
			return Snap.redirect('/club/%s/' % real_name)
		club = ClubSnap.club_find_by_sname(sname)

		if club == None :
			raise Http404("或许你希望创建一个社团？")

		dict_render['visitors'] = AccountSnap.visit_count_by_account(club)
		if request.GET.get('qrcode') == 'true' :	# 统计 qrcode 访问
			log_file_path = settings.MEDIA_ROOT + 'club-qrcode-log.txt'
			log_file = open(log_file_path, 'a', encoding="UTF-8")
			try :
				print(club.id, sname, club.full_name, datetime.now(), 
					request.user.id, request.user.first_name, 
					sep='\t', file=log_file)
			except AttributeError :
				print(club.id, sname, club.full_name, datetime.now(), 
					0, '', sep='\t', file=log_file)
		# 社团页面存在
		time_update = ChineseSnap.datetime_simp(club.time_update)
		dict_render.update({'club': club, 'time_update': time_update, })
		dict_render.update(BadgeDicts.intro('club', club.id))
		dict_render.update(CenterDicts.status(club))
		dict_render['title'] = t_(' - %s的主页') % dict_render['club'].full_name
		dict_render['club_follower_total'] = ClubSnap.follower_total(
			club.id)
		dict_render['share_box'] = []
		for i in ShareSnap.share_find_by_aid('club', club.id)[:10] :
			date_time = ChineseSnap.datetime_simp(i.time_create)
			dict_render['share_box'].append({
				'link': '/share/%s/' % i.attach_uuid, 
				'date': date_time[0], 
				'data': i, 
				'time': date_time[1], 
			})
		dict_render['presentation_list'] = ShareSnap.presentation_find_by_aid \
			('club', club.id, 'large', 10)
		dict_render['picture'] = CenterDicts.club_picture(club.id, ('qrcode', ))

		# follower_list
		follower_qry = ClubSnap.follower_find(club.id)
		follower_nickname = []
		for i in follower_qry[:6] :
			follower_nickname.append({
				'nickname': UserSnap.nickname_find_by_uid(i.account_id_A)[:5], 
				'avatar': AvatarSnap.avatar_find \
					('user', i.account_id_A, 'medium'), 
				'sname': UserSnap.sname_find_by_uid(i.account_id_A), 
			})
		dict_render['follower_list'] = follower_nickname
		dict_render['title'] = t_(' - %s') % club.full_name
		dict_render['club_member_total'] = ClubSnap.member_total(club.id)
		if ClubSnap.sname_verify(request, sname, True) == True:
			# 用户为社长并且不需要预览
			if ClubSnap.sname_verify(request, sname) == True :
				if dict_render['avatar'].startswith('/static/') :
					if random.randint(1, 3000) % 2 : 			# 强制上传头像
						return Snap.redirect('/avatar/club/%s/' % sname)
			dict_render['inc_admin'] = ClubSnap.sname_verify(request, sname)
			dict_render['joined'] = True
			dict_render.update(EventDicts.club_admin(club, dict_render))
			dict_render.update(ShareDicts.club_admin(club, dict_render))
			dict_render['alias_list'] = ClubSnap.alias_all_by_cid(club.id)
			return Snap.render('club_admin.html', dict_render)
		else :
			dict_render['inc_admin'] = False
			dict_render.update(EventDicts.club(request, club))
			uid = UserSnap.uid_find_by_request(request)
			dict_render['followed'] = ClubSnap.club_followed_by_uid(uid, 
															club.id)
			dict_render['joined'] = ClubSnap.club_joined_by_uid(uid, 
															club.id).exists()
			dict_render['core'] = \
				ClubSnap.club_position_by_uid(club.id, uid)[0] == 'core'
			return Snap.render('club_view.html', dict_render)

	@vary_on_cookie
	@UserAuthority.logged_in
	def user_redirect(request) :
		"重定向到用户主页"
		dict_render = UserAgentSnap.record(request)
		if request.user.is_authenticated():
			return Snap.redirect('/user/%s/#%s' %
					(request.user.last_name, request.GET.get('redirect', '')))
		else :
			return Snap.redirect('/login/')

	@vary_on_cookie
	def user_show(request, sname) :
		dict_render = UserAgentSnap.record(request)
		uid = UserSnap.uid_find_by_sname(sname)
		user = UserSnap.user_find_by_uid(uid)
		visitor_id = UserSnap.uid_find_by_request(request)
		if not user :
			raise Http404('找不到用户')
		dict_render['title'] = t_(' - %s的主页') % user.first_name
		dict_render['user'] = user
		dict_render['club_join'] = []
		dict_render['club_follow'] = []
		club = list(ClubSnap.club_find_by_uid(uid))
		club += list(ClubSnap.club_find_by_uid(uid, False))
		for i in set(club) :
			event = EventSnap.event_find_by_cid('club', i.id)
			event_list = []
			for j in list(event)[-3:] :
				evtime = ChineseSnap.datetime_simp(j.time_create)
				event_list.append({
					'data': j, 
					'datetime': evtime[0] + evtime[1], 
					'join': EventSnap.signup_total(j.id), 
				})
			member = ClubSnap.member_all(i.id)
			member_nickname = []
			for j in list(member)[:3] :
				member_nickname.append(UserSnap.nickname_find_by_uid(j))
			follower_qry = ClubSnap.follower_find(i.id)
			follower_nickname = []
			for j in follower_qry[:3] :
				follower_nickname.append \
					(UserSnap.nickname_find_by_uid(j.account_id_A))
			position = ClubSnap.club_position_by_uid(i.id, uid)
			club_dict = {
				'data': i, 
				'position': position[1],
				'event_list': sorted(event_list, 
							key=lambda x: x['data'].time_set, reverse=True), 
				'event_num': event.count(), 
				'member_nickname': t_('，').join(member_nickname), 
				'member_num': len(member), 
				'member_gt_3': len(member) > 3, 
				'follower_nickname': t_('，').join(follower_nickname), 
				'follower_num': follower_qry.count(), 
				'follower_gt_3': follower_qry.count() > 3, 
				'avatar': AvatarSnap.avatar_all('club', i.id), 
				'visitor_join': ClubSnap.club_position_by_uid \
					(i.id, UserSnap.uid_find_by_request(request))[0] != 'none', 
			}
			if position[0] != 'none' :
				dict_render['club_join'].append(club_dict)
			if ClubSnap.club_followed_by_uid(uid, i.id) :
				dict_render['club_follow'].append(club_dict)
		dict_render['title'] = t_(' - %s的主页') % user.first_name
		account = UserSnap.account_find_by_uid(uid)
		dict_render['visit_count'] = AccountSnap.visit_count_by_account(account)
		dict_render['join_time'] = ChineseSnap.timedelta_simp \
			(datetime.now() - user.date_joined)
		if UserSnap.sname_find_by_request(request) == sname :	# user_admin
			dict_render['inc_admin'] = True
			dict_render['user_avatar'] = AvatarSnap.avatar_all('user', uid)
			if dict_render['user_avatar']['raw'].startswith('/static/') :
				if random.randint(1, 3000) % 3 == 0 :			# 强制上传头像
					return Snap.redirect('/avatar/user/%s/' % sname)
			dict_render.update(BadgeDicts.intro('user', uid))
			dict_render.update(CenterDicts.club_find(uid))
			dict_render['nickname'] = UserSnap.nickname_find_by_uid(uid)
			dict_render['badge_list'] = BadgeDicts.badge_find('user', uid)
			dict_render['contact_club'] = dict_render['club_join']
			dict_render['contact_user'] = []
			for i in UserSnap.contact_list(uid) :
				data = UserSnap.user_find_by_uid(i)
				dict_render['contact_user'].append({
					'data': data, 
					'avatar': AvatarSnap.avatar_all('user', i), 
					'nickname': UserSnap.nickname_find_by_uid(i), 
				})
			dict_render['share_list'] = []
			share_qry = ShareSnap.share_find_by_aid('user', uid)
			for i in share_qry :
				dict_render['share_list'].append({
					'data': i, 
					'date': ChineseSnap.datetime_simp(i.time_create), 
				})
			dict_render['tab_active'] = request.GET.get('tag', 'messages')
			dict_render['tab_list'] = [
				('messages', '消息', ), 
				('club', '我的社团', ), 
				('follow', '订阅列表', ), 
				('footprint', '我的足迹', ), 
				('friends', '好友动态', ), 
				('share', '我的分享', ), 
				('settings', '设置', ), 
			]
			dict_render['system_avatar'] = AvatarSnap.avatar_all('system', 0)
			return Snap.render('user_admin.html', dict_render)
		else :	# user_view
			user = UserSnap.user_find_by_uid(uid)
			club = list(ClubSnap.club_find_by_uid(uid, True)) + \
					list(ClubSnap.club_find_by_uid(uid, False))
			dict_render['followed'] = UserSnap.is_follower(uid, visitor_id)
			dict_render['friend'] = UserSnap.is_friend(uid, visitor_id)
			friend_status = UserSnap.friend_status_find(uid, visitor_id)
			dict_render['friend_status'] = friend_status
			if friend_status == 'friend' :
				dict_render['friend_status_text'] = t_('取消好友')
				dict_render['friend_active_tag'] = ''
				dict_render['friends'] = True
			elif friend_status == 'friend-waiting' :	#visitor等待
				dict_render['friend_status_text'] = t_('正在等待对方审核')
				dict_render['friend_active_tag'] = 'active'
			elif friend_status == 'friend-waiting-reverse' :	#visitor需要确认
				dict_render['friend_status_text'] = t_('同意申请')
				dict_render['friend_active_tag'] = ''
				dict_render['friend_need_verify'] = True
			else :	# none
				dict_render['friend_status_text'] = t_('加为好友')
				dict_render['friend_active_tag'] = ''
			event_list = []
			for event in list(EventSnap.event_find_by_uid(uid))[:10] :
				event_time = list(ChineseSnap.datetime_simp(event.time_set))
				event_time[0] = event_time[0][:-1]
				event_dict = {
					'club': ClubSnap.club_find_by_cid(event.account_id), 
					'club_avatar': AvatarSnap.avatar_all \
						('club', event.account_id), 
					'data': event, 
					'join_num': EventSnap.signup_total(event.id), 
					'datetime': event_time, 
				}
				if event.time_set < datetime.now() :
					event_list.append(event_dict)
				elif not 'event_next' in dict_render :
					dict_render['event_next'] = event_dict
			dict_render['event_list'] = event_list
			dict_render['nickname'] = UserSnap.nickname_find_by_uid(uid)
			dict_render['avatar'] = AvatarSnap.avatar_all('user', uid)
			return Snap.render('user_view.html', dict_render)

	@vary_on_cookie
	def member_set(request, sname) :
		'''
			type		comment
			====		=======
			core		加入核心小组
			vice		变为副社长
			head		社长交接
			member		转正为新社员
			reject		申请被拒绝
			remove		移除社员
		'''
		dict_render = UserAgentSnap.record(request)
		real_name = ClubSnap.alias_find_by_sname(sname)
		if real_name != sname and real_name :
			return Snap.redirect('/club/%s/alter/' % real_name)
		set_type = request.POST.get('type', '')
		cid = ClubSnap.cid_find_by_sname(sname)
		UserAuthority.assert_permission(request, 'club', cid)
		if set_type in ('vice', 'head') :
			fname = request.POST.get('fname', '')
			if set_type == 'vice' :
				ClubSnap.vice_change(cid, fname)
				PublicMessageAction.save(request, 'member', 'vice', 
					UserSnap.uid_find_by_fname(fname), 'user', cid, 'club')
				return Snap.success(request, t_('成功将%s设置为副社长') % fname, 
									{ 'reload': True })
			else :
				ClubSnap.head_change(cid, fname)
				PublicMessageAction.save(request, 'member', 'head', 
					UserSnap.uid_find_by_fname(fname), 'user', cid, 'club')
				url = '/club/%s/' % sname
				return Snap.success(request, 
									t_('成功将%s设置为社长') % fname, 
									{ 'redirect': url })
		else :
			function_dict = {
				'core':		ClubSnap.member_core, 
				'member':	ClubSnap.wait_member, 
				'reject':	ClubSnap.wait_reject, 
				'remove':	ClubSnap.member_remove, 
			}
			uid = int(request.POST.get('uid', '0'))
			if not set_type in function_dict :
				raise Snap.error('参数错误')
			result = function_dict[set_type](cid, uid)
			if set_type == 'core' :
				if result :
					PublicMessageAction.save	\
						(request, 'member', 'core', uid, 'user', cid, 'club')
				else :
					fname = ClubSnap.fname_find_by_cid(cid)
					PrivateMessageAction.save \
						('你被降级为%s的普通社员' % (fname), 
							cid, 'club', uid, 'user', cid, 'club')
				return Snap.success(request, '操作成功，请刷新页面')
			if result :
				if set_type == 'member' :
					PublicMessageAction.save(request, 'member', 'new', 
						uid, 'user', cid, 'club')
				elif set_type == 'remove' :
					PrivateMessageAction.save \
						('您已被%s除名' % ClubSnap.fname_find_by_cid(cid), 
							cid, 'club', uid, 'user', cid, 'club')
				return Snap.success(request, '操作成功，请刷新页面')
			else :
				raise Snap.error('操作失败')

	@vary_on_cookie
	def member_manage(request, sname) :
		dict_render = UserAgentSnap.record(request)
		dict_render['sname'] = sname
		real_name = ClubSnap.alias_find_by_sname(sname)
		if real_name != sname and real_name :
			return Snap.redirect('/club/%s/manage/' % real_name)
		aid = ClubSnap.cid_find_by_sname(sname)
		UserAuthority.assert_permission(request, 'club', aid)
		dict_render.update(CenterDicts.member_manage('club', aid))
		fname = ClubSnap.fname_find_by_cid(aid)
		dict_render['title'] = t_(' - %s - 成员管理') % fname
		return Snap.render('club_member_manage.html', dict_render)

	@vary_on_cookie
	def detail(request, src, sname) :
		dict_render = UserAgentSnap.record(request)
		if src == 'user' and UserSnap.sname_find_by_request(request) != sname :
			raise Snap.error('您没有权限')
		if src == 'club' :
			real_name = ClubSnap.alias_find_by_sname(sname)
			if real_name != sname and real_name :
				return Snap.redirect('/club/%s/detail/' % real_name)
		category_default = {'user': 'inbox', 'club': 'event'}[src]
		category = request.GET.get('category', category_default)
		if src == 'user' or category not in ('event', 'share') :
			raise Http404()		# 可能造成攻击，目前不启用相关功能
		if category not in ('sent', 'inbox', 'follow', 'event', 'share') :
			category = category_default
		aid = AccountSnap.aid_find_by_sname(src, sname)
		dict_render['category'] = category
		query_dict = {
			'sent': lambda: PrivateMessage.objects.filter \
								(send_id=aid, send_relation=src), 
			'inbox': lambda: PrivateMessage.objects.filter \
								(recv_relation=src, recv_id=aid), 
			'follow': lambda: PrivateMessage.objects.filter(recv_id=aid, 
								recv_relation=src, send_relation='club'), 
			'event': lambda: EventInfo.objects.filter(account_id=aid, 
								category__in=('history', ''), relation=src), 
			'share': lambda: ShareInfo.objects.filter \
								(status=0, account_id=aid, relation=src), 
		}
		qry = query_dict[category]().order_by('-time_create')
		sliced = AuthDicts.page_dict(request, qry, 8, dict_render)
		dict_render['detail_list'] = CenterDicts.detail(src, sliced, category)
		fname = ClubSnap.fname_find_by_cid(aid)
		c_translate = {
			'sent': t_('发件箱'), 'inbox': t_('收件箱'), 'follow': t_('订阅社团'), 
			'share': t_('分享'), 'event': t_('活动'), 
		}
		dict_render['title'] = t_(' - %s - %s') % (fname, c_translate[category])
		return Snap.render('detail.html', dict_render)

	@vary_on_cookie
	def signature_modify(request, sname) :
		'/user/([A-Za-z\-]+)/signature/ 更改用户签名/动态'
		dict_render = UserAgentSnap.record(request)
		uid = UserSnap.uid_find_by_request(request)
		sign = request.POST.get('signature', '')
		if not uid :
			raise Snap.error('您尚未登录天台')
		if not sign :
			raise Snap.error('动态不能为空')
		if UserSnap.signature_modify(uid, sign) :
			PublicMessageAction.save \
				(request, 'user', 'update', uid, 'user', uid, 'signature')
			return Snap.success(request, '成功更新动态')
		else :
			raise Snap.error('动态请求有误')

	@vary_on_cookie
	def follower_list(request, sname) :
		'/club/[sname]/follower/'
		dict_render = UserAgentSnap.record(request)
		real_name = ClubSnap.alias_find_by_sname(sname)
		if real_name != sname and real_name :
			return Snap.redirect('/club/%s/follower/' % real_name)
		aid = AccountSnap.aid_find_by_sname('club', sname)
		qry = ClubSnap.follower_find(aid)
		follower_list = []
		for i in qry :
			follower_list.append({
				'data': UserSnap.user_find_by_uid(i.account_id_A), 
				'avatar': AvatarSnap.avatar_all('user', i.account_id_A),
				'nickname': UserSnap.nickname_find_by_uid(i.account_id_A)[:5], 
			})
		dict_render['follower_list'] = follower_list
		fname = ClubSnap.fname_find_by_cid(aid)
		dict_render['title'] = t_(' - %s - 订阅用户') % fname
		return Snap.render('club_follower.html', dict_render)

	@vary_on_cookie
	def album_show(request, sname) :
		dict_render = UserAgentSnap.record(request)
		real_name = ClubSnap.alias_find_by_sname(sname)
		if real_name != sname and real_name :
			return Snap.redirect('/club/%s/album/' % real_name)
		cid = ClubSnap.cid_find_by_sname(sname)
		dict_render['presentation_list'] = ShareSnap.presentation_find_by_aid \
				('club', cid, 'exlarge')
		fname = ClubSnap.fname_find_by_cid(cid)
		dict_render['title'] = t_(' - %s - 相册') % fname
		return Snap.render('club_album.html', dict_render)

class ClubSiteMap(Sitemap) :
	def items(self) :
		return ClubAccount.objects.all()
	def location(self, item) :
		return '/club/%s/' % item.simp_name

class UserSiteMap(Sitemap) :
	def items(self) :
		return User.objects.all()
	def location(self, item) :
		return '/user/%s/' % item.last_name


from .models import *

class PublicMessageAction :
	def prompt_create_en(source, action) :
		if source == 'event' :
			return {
				'new': 		' creates a new event ', 
				'nice': 	' likes event ', 
				'follow': 	' prepares to join ', 
				'delete': 	' deletes an event ', 
			}[action]
		elif source == 'share' :
			return {
				'new':		'posts a new share', 
				'knowledge':'posts a brief news', 
			}[action]
		elif source == 'signup' :
			return {
				'new':		' creates sign up of event ', 
				'success': 	' successfully signs up for ', 
			}[action]
		elif source == 'member' :
			return {
				'new':		'\'s membership is verified by ', 
				'delete': 	' quits ', 
				'core': 	' becomes core member of ', 
				'head': 	' becomes the president of ', 
				'vice': 	' is assigned as vice president '
												'of ', 
				'normal': 	' becomes a normal member at ', 
				'apply': 	' applies to join ', 
			}[action]
		elif source == 'club' :
			return {
				'new': 		' creates a new club ', 
				'update': 	' updates introduction of ', 
				'follow': 	' follows ', 
				'avatar': 	' updates avatar of ', 
			}[action]
		elif source == 'badge' :
			return {
				'new': 		' creates a new badge ', 
				'create': 	' creates a new badge ', 
				'grant': 	' receives badge ', 
			}[action]
		elif source == 'user' :
			return {
				'new': 		' registers in BNDS Circle ', 
				'follow': 	' follows user ', 
				'edit': 	' modifies personal profile ', 
				'update': 	' updates status ', 
				'avatar': 	' updates avatar', 
			}[action]
		elif source == 'news' :
			return {
				'new': 		' creates news ', 
			}[action]
		elif source == 'empty' :
			return {
				'new': 		' submits rating profile to ', 
				'granted': 	'\'s rating profile is admitted', 
				'fine': 	'\'s rating profile is not admitted', 
			}[action]
		elif source == 'forum' :
			return {
				'thread':	' creates thread ', 
				'response': ' replies thread ', 
			}[action]
		return {}

	def prompt_create(source, action) :
		mcim = lambda **x: x
		if get_language() == 'en' :
			return mcim(body=PublicMessageAction.prompt_create_en(source, 
																	action))
		if source == 'event' :
			return {
				'new': 		lambda: mcim(body='创建了一个新活动'), 
				'nice': 	lambda: mcim(body='喜欢活动'), 
				'follow': 	lambda: mcim(body='准备参加活动'), 
				'delete': 	lambda: mcim(body='删除了一个活动'), 
			}[action]()
		elif source == 'share' :
			return {
				'new':		lambda: mcim(body='推送了一个新分享'), 
#				'hot': 		lambda: mcim(head='热门分享：'), 
				'knowledge':lambda: mcim(body='社团发布了快讯 - '), 
			}[action]()
		elif source == 'signup' :
			return {
				'new':		lambda: mcim(body='创建了活动', tail='的签到'), 
				'success': 	lambda: mcim(body='成功签到活动'), 
			}[action]()
		elif source == 'member' :
			return {
				'new':		lambda: mcim(body='通过', tail='社团的加入审核'), 
				'delete': 	lambda: mcim(body='退出了'), 
				'core': 	lambda: mcim(body='晋升为', tail='的核心成员'), 
				'head': 	lambda: mcim(body='被交接为', tail='的社长'), 
				'vice': 	lambda: mcim(body='被钦定为', tail='的副社长'), 
				'normal': 	lambda: mcim(body='在', tail='下野，成为庶民'), 
				'apply': 	lambda: mcim(body='申请加入'), 
			}[action]()
		elif source == 'club' :
			return {
				'new': 		lambda: mcim(body='创建了新社团'), 
				'update': 	lambda: mcim(body='更新了', tail='的社团资料'), 
				'follow': 	lambda: mcim(body='订阅了'), 
				'avatar': 	lambda: mcim(body='更新了头像'), 
			}[action]()
		elif source == 'badge' :
			return {
				'new': 		lambda: mcim(body='创建了新徽章'), 
				'create': 	lambda: mcim(body='创建了新徽章'), 
				'grant': 	lambda: mcim(body='被授予徽章'), 
			}[action]()
		elif source == 'user' :
			return {
				'new': 		lambda: mcim(head='新成员', body='落户十一圈'), 
				'follow': 	lambda: mcim(body='跟随用户'), 
				'edit': 	lambda: mcim(body='修改了个人资料'), 
				'update': 	lambda: mcim(body='更新了状态'), 
				'avatar': 	lambda: mcim(head='用户', body='更新了头像'), 
			}[action]()
		elif source == 'news' :
			return {
				'new': 		lambda: mcim(body='创建了新闻'), 
			}[action]()
		elif source == 'empty' :
			return {
				'new': 		lambda: mcim(body='向', tail='提交了星级评价申请'), 
				'granted': 	lambda: mcim(body='的星级评价申请被', tail='审核通过'), 
				'fine': lambda: mcim(body='的星级评价申请没有被', tail='审核通过'), 
			}[action]()
		elif source == 'forum' :
			return {
				'thread':	lambda: mcim(body='创建了帖子'), 
				'response': lambda: mcim(body='回复了帖子'), 
			}[action]()
		return {}

	def save(request, relation, action, major_id, major_src, 
		minor_id=0, minor_src='') :
		from quan_ua.views import UserAgentSnap, Snap
		platform = UserAgentSnap.platform_find(request)
		qry_exist = GlobalMessage.objects.filter(status=0, relation=relation, 
			action=action, major_id=major_id, major_relation=major_src, 
			minor_id=minor_id, minor_relation=minor_src, data='')
		if qry_exist :
			GlobalMessage.objects.filter(id=qry_exist[0].id).update \
					(time_create=datetime.now(), platform=platform)
		else :
			qry = GlobalMessage \
				(status=0, relation=relation, action=action, major_id=major_id, 
				major_relation=major_src, minor_id=minor_id, 
				minor_relation=minor_src, platform=platform)
			qry.save()

	def find(status, time_create, uid, relation) :
		'查找公共消息，返回 按照time_create 正序排序的 迭代器'
		if status == 1 :
			qr = GlobalMessage.objects.filter(time_create__gt=time_create, 
											status=0).order_by('time_create')
			return PublicMessageAction.relation_filter(qr, uid, relation)
		q = GlobalMessage.objects.filter(status=0)
		if status == -1 :
			q = q.filter(time_create__lt=time_create)
		qr = itertools.islice(q.order_by('-time_create'), 10000)	# 防止爆炸
		qry = PublicMessageAction.relation_filter(qr, uid, relation)
		return reversed(tuple(itertools.islice(qry, 16)))

	def account_info_find(src, aid) :
		'''
			得到用户/社团的信息字典（为了返回json消息）
		'''
		from quan_avatar.views import AvatarSnap
		from quan_account.views import UserSnap, ClubSnap, AccountSnap
		from quan_forum.views import ForumSnap
		default = { 'link': '', 'text': '', 'image': '', }
		if src == 'club' :
			return {
				'link':		'/club/%s/' % ClubSnap.sname_find_by_cid(aid), 
				'text':		ClubSnap.fname_find_by_cid(aid), 
				'image':	AvatarSnap.avatar_find('club', aid, 'small'), 
			}
		elif src == 'user' :
			return {
				'link':		'/user/%s/' % UserSnap.sname_find_by_uid(aid), 
				'text':		UserSnap.nickname_find_by_uid(aid), 
				'image':	AvatarSnap.avatar_find('user', aid, 'small'), 
			}
		elif src == 'event' :
			from quan_event.views import EventSnap
			event = EventSnap.event_find_by_evid(aid)
			if not event :
				return default
			cid = event.account_id
			return {
				'link':		'/event/%d/' % aid, 
				'text':		event.subject, 
				'image':	AvatarSnap.avatar_find('club', cid, 'small'), 
			}
		elif src == 'share' :
			from quan_share.views import ShareSnap
			share = ShareSnap.share_find_by_sid(aid)
			if not share :
				return default
			suid = share.attach_uuid
			return {
				'link':		'/share/%s/' % suid, 
				'text':		share.subject, 
				'image':	ShareSnap.thumbnail_find(suid, 'small') or \
							AvatarSnap.avatar_find \
								(share.relation, share.account_id, 'small'), 
			}
		elif src == 'badge' :
			from quan_badge.views import BadgeSnap
			badge = BadgeSnap.badge_find_by_bid(aid)
			if not badge :
				return default
			sname = ClubSnap.sname_find_by_cid(badge.account_id)
			return {
				'link':		'/club/%s/' % sname, 
				'text':		badge.name, 
				'image':	None, 
			}
		elif src == 'news' :
			from quan_news.views import NewsSnap
			news = NewsSnap.news_find(aid)
			if not news :
				return default
			return {
				'link':		'/news/%d/' % aid, 
				'text':		news.subject, 
				'image':	None, 
			}
		elif src == 'signature' :
			user = UserSnap.user_find_by_uid(aid)
			if not user :
				return default
			return {
				'link':		'/user/%s/' % user.last_name, 
				'text':		UserSnap.signature_find_by_uid(aid), 
				'image':	None, 
			}
		elif src == 'nickname' :
			user = UserSnap.user_find_by_uid(aid)
			if not user :
				return default
			return {
				'link':		'/user/%s/' % user.last_name, 
				'text':		UserSnap.nickname_find_by_uid(aid), 
				'image':	None, 
			}
		elif src == 'forum_thread' :
			thread = ForumSnap.thread_find_by_thid(aid)
			sname = ForumSnap.sname_find_by_gid(thread.group_id)
			return {
				'link':		'/forum/%s/%d/' % (sname, aid), 
				'text':		thread.subject, 
				'image':	None, 
			}
		elif src == 'forum_response' :
			thid = ForumSnap.thid_find_by_rid(aid)
			thread = ForumSnap.thread_find_by_thid(thid)
			sname = ForumSnap.sname_find_by_gid(thread.group_id)
			return {
				'link':		'/forum/%s/%d/?response=%d#response-%d' % \
											(sname, thid, aid, aid), 
				'text':		thread.subject, 
				'image':	None, 
			}
		else :
			return default

	def wrap(qry) :
		from quan_ua.views import ChineseSnap
		message_list = []
		for i in qry :
			message = {
				'id': int(i.time_create.timestamp()), 
				'platform': i.platform, 
				'time_ago': ChineseSnap.timedelta_simp \
							(datetime.now() - i.time_create), 
				'major': PublicMessageAction.account_info_find \
							(i.major_relation, i.major_id), 
				'minor': PublicMessageAction.account_info_find \
							(i.minor_relation, i.minor_id), 
				'time_stamp': i.time_create.timestamp(), 
			}
			message.update(PublicMessageAction.prompt_create
														(i.relation, i.action))
			message_list.append(message)
		return message_list

	def relation_filter(origin, uid, relation) :
		'''
			此函数位于 PublicMessageAction
			处理的情况（可以叠加）: ('', 'all', 'self', 'friend', 'follower')
			此函数返回 yield 体，不打乱顺序
		'''
		if 'friend' in relation :
			from quan_account.views import UserSnap
			friend_list = UserSnap.contact_list(uid)
		if 'follower' in relation :
			from quan_account.views import UserSnap
			following_list = UserSnap.following_find(uid)
		for i in origin :
			if not relation or 'all' in relation :
				yield i; continue
			if 'self' in relation :
				if i.major_relation == 'user' and i.major_id == uid :
					yield i; continue
			if i.major_relation == 'user' :
				if 'friend' in relation and i.major_id in friend_list :
					yield i; continue
				if 'follower' in relation and i.major_id in following_list :
					yield i; continue

class PrivateMessageAction :
	def save(content, conn_id, conn_relation, recv_id, recv_relation, 
		send_id, send_relation) :
		'保存等待推送的PrivateMessage'
		PrivateMessage(content=content, conn_id=conn_id, 
						conn_relation=conn_relation, recv_id=recv_id, 
						recv_relation=recv_relation, send_id=send_id, 
						send_relation=send_relation, status='active').save()

	def follower_send(cid, content, conn_id, conn_src) :
		'传送给社团的follower，传送send默认为cid的club'
		from quan_account.views import ClubSnap
		for i in ClubSnap.follower_list(cid, 'id') :
			PrivateMessageAction.save \
				(content, conn_id, conn_src, i, 'user', 0, 'system')

	def find(status, time_create, recv_id, send_src, send_id, limit) :
		'''
			这个函数只处理『寻找用户的某个群组』
			返回一个 generator ，根据 limit 截取
			情况
				A	自己
				B	另一个用户
				C	自己所属的一个社团
				system
					? -> A		# friend / hi / leave
					S -> A
				user
					A -> B
					B -> A
				club
					C -> A		# 注意：要排除 C -> B
					A -> C
					B -> C
					C -> C
		'''
		recv_src = 'user'
		base = PrivateMessage.objects.filter(deleted=0)
		base_qry = {
			0: lambda x: base, 
			1: lambda x: base.filter(time_create__gte=x), 
			-1: lambda x: base.filter(time_create__lt=x), 
		}[status](time_create)
		if send_src == 'system' :
			ans = base_qry.filter(Q(send_relation='system', send_id=0) | 
								Q(conn_relation__in=('friend', 'hi', 'leave')), 
								recv_relation=recv_src, recv_id=recv_id)
		elif send_src == 'user' :
			ans = base_qry.filter(Q(recv_relation=recv_src, recv_id=recv_id, 
									send_relation=send_src, send_id=send_id) | 
									Q(recv_relation=send_src, recv_id=send_id, 
									send_relation=recv_src, send_id=recv_id))
		elif send_src == 'club' :
			ans = base_qry.filter(Q(recv_relation=send_src, recv_id=send_id) | 
									Q(send_relation=send_src, send_id=send_id, 
									recv_relation=recv_src, recv_id=recv_id))
		else :
			raise Http404('参数错误，请联系HCC社团以解决')
		# 切片和返回
		answer = filter(lambda x: PrivateMessageAction.get_host(x, recv_id), 
						ans.order_by('-time_create'))
		if status == 1 :
			return answer
		else :
			return itertools.islice(answer, limit)

	def all(status, time_create, recv_id, limit) :
		'''
			这个函数找出和用户相关的所有群组的信息
		'''
		recv_src = 'user'
		base = PrivateMessage.objects.filter(deleted=0)
		base_qry = {
			0: lambda x: base, 
			1: lambda x: base.filter(time_create__gte=x), 
			-1: lambda x: base.filter(time_create__lt=x), 
		}[status](time_create)
		# 从和『自己』或者『所属社团』有关的地方搜索
		from quan_account.views import AccountSnap
		contact_list = AccountSnap.contact_list(recv_id)
		cid_list = list(map(lambda x: x[1], 
							filter(lambda x: x[0] == 'club', contact_list)))
		stack = base_qry.filter(Q(send_relation=recv_src, send_id=recv_id) | 
								Q(recv_relation=recv_src, recv_id=recv_id) | 
								Q(recv_relation='club', recv_id__in=cid_list))
		answer_dict = { ('system', 0): [] }
		collections.deque(map(lambda x: answer_dict.__setitem__(x, []), 
								contact_list), 0)
		for index, i in enumerate(stack.order_by('-time_create')) :
			if all(map(lambda x: len(x) >= limit, answer_dict.values())) :
				break
			if index > 1000 and (index > 2000 or all(answer_dict.values())) :
				break	# 防止爆炸
				# 统计信息: 如果网站没有执行这个，可能需要计算 6986 次，耗用 0.428505 秒
				# 			执行后最坏情况大约需要 0.355753 秒
			host = PrivateMessageAction.get_host(i, recv_id)
			if host in answer_dict :
				target = answer_dict[host]
				len(target) < 4 and target.append(i)
		return answer_dict

	def get_host(qry, recv_id) :
		'qry 为一个 PrivateMessage ， recv_id 是查询者，返回 (host_src, host_id)'
		if qry.conn_relation in ('friend', 'hi', 'leave') :
			if recv_id != qry.recv_id :		return None		# 必须单向
			else :							return 'system', 0
		if qry.send_relation == 'system' :	return 'system', 0
		if qry.send_relation == 'club' :	return 'club', qry.send_id
		if qry.recv_relation == 'club' :	return 'club', qry.recv_id
		if qry.send_id == recv_id :			return 'user', qry.recv_id
		if qry.recv_id == recv_id :			return 'user', qry.send_id
		assert not '出现这种情况'

	def link_find(message) :
		'''
			查找链接
		'''
		from quan_account.views import UserSnap, ClubSnap, AccountSnap
		relation = message.conn_relation
		minor_id = message.send_id
		try :
			if relation in ('event', 'signup') :
				return '/event/%d/' % minor_id
			elif relation == 'badge' :
				from quan_badge.views import BadgeSnap
				qry = BadgeSnap.badge_find_by_bid(bid)
				return '/club/%s/' % ClubSnap.sname_find_by_cid(qry.account_id)
			elif relation in ('member', 'club') :
				sname = ClubSnap.sname_find_by_cid(minor_id)
				return '/club/%s/' % sname
			elif relation in ('share', 'comment') :
				suid = ShareSnap.uuid_find_by_sid(minor_id)
				return '/share/%s/' % suid
			elif relation == 'user' :
				sname = UserSnap.sname_find_by_uid(major_id)
				return '/user/%s/' % sname
			elif relation == 'news' :
				return '/news/%d/' % minor_id
			else :
				return '#'
		except Exception as e :
			print(e)
			return '#error'

	def chat_wrap(qry, recv_id) :
		'''
			为 PrivateMessage 写的 qry->list 函数
			其中 send_src 和 send_id 表明期望的 host_id
			返回 yield 体
		'''
		from quan_event.views import EventSnap
		from quan_avatar.views import AvatarSnap
		from quan_account.views import ClubSnap, AccountSnap, UserSnap
		from quan_ua.views import ChineseSnap
		message_list = []
		for i in qry :
			# user A = 自身
			# user B = 好友
			# club C = 一个社团
			# 可能出现的情况	host	avatar
			#	user
			#		A -> B	 B		A
			#		B -> A	 B		B
			#	club
			#		C -> A	 C		C
			#		A -> C	 C		A
			#		B -> C	 C		B
			host_src, host_id = PrivateMessageAction.get_host(i, recv_id)
			src = i.conn_relation
			if i.send_id == recv_id and i.send_relation == 'user' :
				if src == 'share' :
					src = 'share-self'
				else :
					src = 'self'
			elif src == 'none' :
				src = 'other'
			if i.send_relation == 'user' and src == 'share' :
				src = 'share-other'
			message_dict = {
				'content': i.content, 
				'time_update': ChineseSnap.datetime_simp(i.time_create), 
				'url': PrivateMessageAction.link_find(i), 
				'avatar': AvatarSnap.avatar_all(i.send_relation, i.send_id), 
				'type': src, 
				'host_id': host_id, 
				'host_src': host_src, 
				'time_stamp': i.time_create.timestamp(), 
			}
			aid = i.conn_id
			if src in ('share', 'share-self', 'share-other') :
				from quan_share.views import ShareSnap
				qry = ShareSnap.share_find_by_sid(aid)
				if qry :
					from quan_share.views import ShareSnap
					message_dict.update({
						'data': { 
							'subject': qry.subject, 
							'uuid': qry.attach_uuid
						}, 
						'attach': ShareSnap.file_list_find_by_suid \
													(qry.attach_uuid, True), 
					})
			elif src in ('event', 'event-signup') :
				from quan_event.views import EventSnap
				qry = EventSnap.event_find_by_evid(aid)
				if not qry :
					continue
				club = ClubSnap.club_find_by_cid(qry.account_id)
				if not club :
					continue
				message_dict.update({
					'data': {
						'subject': qry.subject, 
						'location': qry.location, 
						'content': qry.content, 
						'id': qry.id, 
					}, 
					'avatar': AvatarSnap.avatar_all(qry.relation, 
													qry.account_id), 
					'club': { 'full_name': club.full_name }, 
					'date': ChineseSnap.datetime_simp(qry.time_set), 
				})
			elif src == 'badge' :
				from quan_badge.views import BadgeSnap
				qry = BadgeSnap.badge_find_by_bid(aid)
				if not qry :
					continue
				club = ClubSnap.club_find_by_cid(qry.account_id)
				if not club :
					continue
				message_dict.update({
					'name': qry.name, 
					'club': { 'simp_name': club.simp_name }, 
				})
			elif src in ('friend', 'hi') :
				aid = i.send_id
				message_dict.update({
					'avatar': AvatarSnap.avatar_all('user', aid), 
					'nickname': UserSnap.nickname_find_by_uid(aid), 
					'id': aid, 
					'sname': UserSnap.sname_find_by_uid(aid), 
					'disable': '', 
				})
				if AccountSnap.relation_check \
					(recv_id, aid, ('uu-friend', 'uu-friend-wait')) :
					message_dict['disable'] = 'disabled="disabled"'
			elif src == 'leave' :
				message_dict.update({
					'cname': ClubSnap.fname_find_by_cid(i.conn_id), 
					'fname': UserSnap.fname_find_by_uid(i.send_id), 
				})
			else :	# other, self
				message_dict.update({
					'avatar': AvatarSnap.avatar_all(i.send_relation, i.send_id), 
					'nickname': AccountSnap.nickname_find_by_aid \
						(i.send_relation, i.send_id), 
				})
				if i.send_id == recv_id and i.send_relation == 'user' :
					message_dict['type'] = 'self'
			yield message_dict

class MessageSnap:
	def update_situation(request) :
		'''
			return current_stamp, time_create, status
					^	现在			^POST的时间
			status说明:
				-1	更新早于-time_create的最后16条消息
				0	更新最近16条
				1	更新晚于time_create的条目
		'''
		update = request.POST.get('time_update', '')
		if not update :
			update = request.GET.get('time_update', '0')
		float_update = float(update)
		time_current = datetime.now()
		current_stamp = time_current.timestamp()
		try :
			status = 0
			time_create = datetime.fromtimestamp(float_update)
			if float_update > current_stamp - 1800 :
				status = 1
			if float_update < 0 :
				time_create = datetime.fromtimestamp(-float_update)
				status = -1
		except Exception as e :
			time_create = 0
			status = 0
		return current_stamp, time_create, status

	def message_delete(src, aid) :
		'关于分享和活动的删除，返回是否失败'
		if src not in ('share', 'event', 'badge', 'club', 'forum_thread', 
						'forum_response') :
			return False
		#Public / Global
		GlobalMessage.objects.filter(minor_id=aid, minor_relation=src).update \
			(status=1)
		GlobalMessage.objects.filter(major_id=aid, major_relation=src).update \
			(status=1)
		#Private
		PrivateMessage.objects.filter(conn_relation=src, conn_id=aid).update \
			(deleted=1)
		PrivateMessage.objects.filter(recv_relation=src, recv_id=aid).update \
			(deleted=1)
		PrivateMessage.objects.filter(send_relation=src, send_id=aid).update \
			(deleted=1)
		return True

class MessageViews:
	@never_cache
	def private_message_fetch(request) :
		'''
			[JSON] /message/private/
			status说明:
				-1	更新早于-time_create的最后16条消息
				0	更新最近16条
				1	更新晚于time_create的条目
			更新较早信息可以通过返回的time_stamp字段得到最早的信息的时间
		'''
		from quan_ua.views import UserAgentSnap, Snap
		dict_render = UserAgentSnap.record(request)
		if request.method != 'POST' :
			raise Http404('请求方法不正确')
		from quan_account.views import UserSnap, ClubSnap
		uid = UserSnap.uid_find_by_request(request)
		if not uid :
			raise Http403('请先登录')
		current, time_create, status = MessageSnap.update_situation(request)
		send_src = request.POST.get('send_src', '')
		try :
			if send_src not in ('', 'club', 'user', 'system') :
				raise ValueError
			send_id = int(request.POST.get('send_id', '0'))
		except ValueError :
			raise Http404('参数错误')
		# 可能的情况
		#	从 0 更新所有的字段
		#	从 0 更新一个字段
		#	从一分钟前更新所有字段
		#	向前更新一个字段
		limit = 4
		if send_src :
			if send_src == 'club' and send_id not in ClubSnap.contact_list(uid):
				raise Http403('权限错误')
			qry = PrivateMessageAction.find \
							(status, time_create, uid, send_src, send_id, limit)
		else :
			answer = PrivateMessageAction.all(status, time_create, uid, limit)
			qry = itertools.chain.from_iterable(answer.values())
		message_list = list(PrivateMessageAction.chat_wrap(qry, uid))
		
		if message_list :
			time_last = min(message_list, key=lambda x: x['time_stamp']) \
				['time_stamp']
		elif status == -1 :
			time_last = time_create.timestamp()
		else :
			time_last = current
		json_data = {
			'msglist': message_list, 
			'time_update': current, 
			'time_last': time_last, 
		}
		resp = Snap.success(request, '', json_data)
		resp['Access-Control-Allow-Origin'] = 'http://shiyiquan.net'
		return resp

	@never_cache
	def global_message_fetch(request) :
		'''
			[JSON] [GET] /message/global/
			参数 status 说明:
				-1	更新早于 time_lower	的 16 条消息，尽可能晚
				0	更新最新				的 16 条消息
				1	更新晚于 time_upper	的 16 条消息，尽可能早
					# 为了防止攻击，可以考虑将这个值设定限制
			更新较早信息可以通过返回的time_stamp字段得到最早的信息的时间
		'''
		from quan_ua.views import UserAgentSnap, Snap
		dict_render = UserAgentSnap.record(request)
		from quan_account.views import UserSnap, ClubSnap
		if request.method != 'GET' :
			raise Http404('请求方法不正确')
		relation = request.GET.get('relation', '')
		try :
			uid = int(request.GET.get('uid', '0'))
		except ValueError :
			raise Http404('参数错误')
		current, time_create, status = MessageSnap.update_situation(request)
		qry = PublicMessageAction.find(status, time_create, uid, relation)
		message_list = PublicMessageAction.wrap(qry)
		json_data = {
			'msglist': message_list, 
			'time_now': current, 
		}
		if status != -1 :
			json_data['time_update'] = current
		if message_list :
			json_data['time_last'] = message_list[0]['time_stamp'] - 1
		else :
			json_data['time_last'] = 946684800		# 2000 年 1 月 1 日 8 时
		resp = Snap.success(request, '', json_data)
		resp['Access-Control-Allow-Origin'] = 'http://shiyiquan.net'
		return resp

	@vary_on_cookie
	def contact_hi(request) :
		'''
			[POST] user_view 打招呼
			status
				real
				conceal
		'''
		from quan_ua.views import UserAgentSnap, Snap
		dict_render = UserAgentSnap.record(request)
		from quan_account.views import UserSnap
		status = request.POST.get('status', '')
		content = request.POST.get('content', '')
		host_id = request.POST.get('uid', '0')
		sender_id = UserSnap.uid_find_by_request(request)
		if sender_id in ('0', 0, None) :
			raise Snap.error('请先登录')
		if host_id in ('0', 0) :
			raise Snap.error('请指明收件人')
		if status == 'real' or 1 :	# from AccountViews.user_friend
			friend_status = UserSnap.friend_status_find(host_id, sender_id)
			if friend_status == 'friend-waiting-reverse' :	#visitor需要确认
				UserSnap.friend_check(sender_id, host_id)
			elif friend_status == 'none' and not UserSnap.is_friend_annoy \
				(sender_id, host_id) :
				UserSnap.friend_wait(sender_id, host_id)
			sender_id_show = sender_id
			# sender_nickname_show = UserSnap.nickname_find_by_uid(sender_id)
		else :	# conceal, 暂时
			sender_id_show = 0
			# sender_nickname_show = "一个人"
		PrivateMessageAction.save(content, sender_id_show, 'hi', 
			host_id, 'user', sender_id_show, 'user')
		return Snap.success(request, '投递成功')

	@vary_on_cookie
	def message_send(request) :
		from quan_account.views import UserSnap
		from quan_share.views import ShareViews
		from quan_ua.views import UserAgentSnap, Snap
		dict_render = UserAgentSnap.record(request)
		send_id = UserSnap.uid_find_by_request(request)
		if not send_id :
			raise Snap.error('请先登录再发送消息')
		content = request.POST.get('content', '')
		if not content :
			raise Snap.error('不能发送空白消息')
		if request.POST.get('attach_uuid', '') :
			return ShareViews.share_create(request)
		try :
			recv_src = request.POST.get('recv_src', '')
			recv_id = int(request.POST.get('recv_id', '0'))
			if recv_src not in ('club', 'user', 'system') :
				raise ValueError
		except ValueError :
			raise Snap.error('参数错误')
		PrivateMessageAction.save \
			(content, 0, 'none', recv_id, recv_src, send_id, 'user')
		return Snap.success(request, '投递成功')

	@vary_on_cookie
	def message_leave(request) :
		'向社团社长和副社长的系统通知投递对社团的意见'
		from quan_ua.views import UserAgentSnap, Snap
		dict_render = UserAgentSnap.record(request)
		from quan_account.views import UserSnap, ClubSnap
		aid = int(request.POST.get('aid', '0'))
		src = request.POST.get('src', '')
		uid = UserSnap.uid_find_by_request(request)
		if not uid :
			raise Snap.error('您还没有登录')
		content = request.POST.get('content', '')
		if len(content) == 0 :
			raise Snap.error('请写内容')
		for i in ClubSnap.leader_find_by_cid(aid) :
			PrivateMessageAction.save(content, aid, 'leave', i.id, 'user', 
				uid, 'user')
		return Snap.success(request, '投递成功')


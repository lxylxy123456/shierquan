from common import *

from quan_event.models import EventInfo, EventRelation
from quan_account.models import ClubAccount

from quan_account.views import *
from quan_auth.views import AuthSnap, AuthDicts
from quan_avatar.views import AvatarSnap
from quan_event.views import EventSnap
from quan_share.views import ShareSnap
from quan_ua.views import *

class SquareSnap :
	def event_newest() :
		'''
			离现在最近的三个活动，之后的活动优先。时间长度不能超过 18 小时
		'''
		qry = EventInfo.objects.filter(category='')
		current = datetime.now()
		event_sorted = itertools.chain(
			qry.filter(time_end__gte=current).order_by('time_end').iterator(), 
			qry.filter(time_end__lt=current).order_by('-time_end').iterator(), 
		)
		event_filtered = filter(
					lambda x: x.time_end - x.time_set <= timedelta(0, 64800), 
					event_sorted
				)
		return list(itertools.islice(event_filtered, 3))

	def capital_find(club) :
		'simp_name的第一个字符，如果不是字母，返回#'
		try :
			name = pypinyin.lazy_pinyin(club.full_name[0])[0][0].upper()
			if 'A' <= name <= 'Z' :
				return name
		except Exception :
			pass
		return '#'

	def total_rank(club, detail=False) :
		'event + share + watch, 当三无时返回0'
		cid = club.id
		cache_key = 'SquareSnap__total_rank__%d' % cid
		cached = cache.get(cache_key)
		if cached :
			if detail :
				return cached
			else :
				return cached['rank']
		rank = 0
		event_num = EventSnap.event_find_by_cid('club', cid).count()
		share_num = ShareSnap.share_find_by_aid('club', cid).count()
		follower_num = ClubSnap.follower_total(cid)
		avatar_num = int(bool(AvatarSnap.avatar_find('club', cid, '', True)))
		rank += 20 * event_num
		rank += 15 * share_num
		rank += 10 * follower_num
		rank += 30 * avatar_num
		answer = {
			'rank': rank, 
			'event_num': event_num, 
			'share_num': share_num, 
			'follower_num': follower_num, 
			'avatar_num': avatar_num, 
		}
		cache.set(cache_key, answer, random.randint(800000, 900000))
		if detail :
			return answer
		else :
			return rank

class SquareDicts:
	def square_event(data, belong, request) :
		'复制每块的字典'
		item = { 'data': data }
		# 渲染的模块名
		item['belong'] = belong
		# 开始时间
		time_set = data.time_set
		item['day_set'], item['time_set'] = ChineseSnap.datetime_comp(time_set)
		# 头相、赞、关注、发起者
		cid = data.account_id
		item['follower'] = EventSnap.follower_total(data.id)
		item['nice'] = EventSnap.nice_total(data.id)
		item['avatar'] = AvatarSnap.avatar_find(data.relation, cid, 'medium')
		item['sponsor'] = ClubSnap.sname_find_by_cid(cid)
		item['sponsor_fname'] = ClubSnap.fname_find_by_cid(cid)
		# 持续时间
		item['time_last'] = ChineseSnap.timedelta_comp(data.time_end - time_set)
		# 是否已经关注/赞
		item['niced'] = EventSnap.niced_find_by_request(request, data.id)
		item['followed'] = EventSnap.followed_find_by_request(request, data.id)
		return item

	def home_dict_get_6(request, number=6) :
		'相当于原来的 home_dict_get(request, special_passment=True)[:number]'
		#最新，最火
		event_list = []
		for i in EventInfo.objects.filter \
			(category__in=('history', '')).order_by("-time_set")[:number]:
			event_list.append(SquareDicts.square_event(i, 'latest', request))
		return event_list

	def home_dict_get(request, special_passment=False) :
		'得到“我参加的”、“最新”、“最火”，返回一个dict_render体'
		dict_render = {}
		if request.path in ['/square/', '/square/hotest/'] or special_passment :
			#最新，最火
			sliced_qry = AuthDicts.page_dict(request, EventInfo.objects.filter \
				(category__in=('history', '')).order_by("-time_set"), 10, 
				dict_render)
			event_list = []
			for i in sliced_qry:
				event_list.append(SquareDicts.square_event(i, 'latest',request))
			if request.path == '/square/hotest/' and not special_passment :
				a = event_list.sort(
					key = lambda dictionary:-dictionary['follower'])
			dict_render['event_list'] = event_list
			return dict_render
		else :	#我参加的
			event_set = EventSnap.event_filter_by_request(request)
			sliced = AuthDicts.page_dict(request, event_set, 10, dict_render)
			dict_render['event_list'] = []
			for i in sliced :
				dict_render['event_list'].append \
					(SquareDicts.square_event(i, 'relative', request))
			return dict_render

	def club_all(request, qry, category='all') :
		uid = UserSnap.uid_find_by_request(request)
		club_list = []
		for i in qry :
			club_dict = { 'data': i }
			club_dict['avatar'] = AvatarSnap.avatar_all('club', i.id)
			club_dict['follow'] = ClubSnap.follower_total(i.id)
			club_dict['followed'] = ClubSnap.club_followed_by_uid(uid, i.id)
			club_dict['followee'] = list(itertools.islice \
											(ClubSnap.follower_list(i.id), 3))
			club_dict['category'] = ClubSnap.category_exchange(i.category)
			club_list.append(club_dict)
		return club_list

	def home_dict(request) :
		'得到/页面的字典，喜欢=关注'
		dict_render = {}
		#得到3个最新活动
		dict_render['event_list'] = []
		event_qry = SquareSnap.event_newest()
		for i in event_qry :
			event_date, event_time = ChineseSnap.datetime_simp(i.time_set)
			dict_render['event_list'].append({
				'data':		i, 
				'nice':		EventSnap.nice_total(i.id), 
				'date': 	event_date, 
				'time': 	event_time, 
				'niced': 	EventSnap.niced_find_by_request(request, i.id), 
				'sname':	ClubSnap.sname_find_by_cid(i.account_id), 
				'fname':	ClubSnap.fname_find_by_cid(i.account_id), 
			})
		dict_render['club_list'] = []
		club_all = ClubSnap.club_all_find()
		club_list = []
		for i in club_all :
			club_list.append((i, SquareSnap.total_rank(i, True)))
		club_filtered = list(filter(lambda x: all(x[1].values()), club_list))
			# 抵制三无社团
		club_filtered.sort(key=lambda x: x[1]['rank'], reverse=True)
		num = min(3, max(0, len(club_filtered) - 3))
		club_qry = club_filtered[:3] + random.sample(club_filtered[3:], num)
		for club, rank in club_qry :
			dict_render['club_list'].append({
				'data':		club,
				'avatar':	AvatarSnap.avatar_find('club', club.id, 'medium'), 
				'follower':	ClubSnap.follower_total(club.id), 
				'followee': ', '.join(itertools.islice \
										(ClubSnap.follower_list(club.id), 3)), 
				'category': ClubSnap.category_exchange(club.category), 
			})
		# 得到社联通知列表
		dict_render['note'] = ShareSnap.union_record_find()
		if AuthSnap.notice_check(UserSnap.uid_find_by_request(request), 
								dict_render['note']) :
			dict_render['note_read'] = True
		return dict_render

	def wall() :
		'/wall/'
		dict_render = {}
		club_dict = {}
		for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ#" :
			club_dict[letter] = []
		qry = ClubSnap.club_all_find()
		for club in qry :
			club_dict[SquareSnap.capital_find(club)].append({
				'data': club, 
				'avatar': AvatarSnap.avatar_find('club', club.id, 'small'), 
			})
		wall_list = list(club_dict.items())
		wall_list.sort(key=lambda x: { '#': 'a' }.get(x[0], x[0]))
			# 这个 lambda 的含义: 如果是'#'则返回a（会被放到最后），否则返回本身（如'H'）
		dict_render['club_section'] = wall_list
		dict_render['club_num'] = qry.count()
		current_date = ChineseSnap.datetime_simp(datetime.now())
		dict_render['current_date'] = current_date[0] + current_date[1]
		return dict_render

	def search_dicts(query, category) :
		'''
			category in ('share', 'event', 'club')
			返回 yield 体
		'''
		if category == 'share' :
			for i in ShareSnap.share_search(query) :
				yield {
					'data': i, 
					'avatar': 
						ShareSnap.thumbnail_find(i.attach_uuid, 'medium') or \
						AvatarSnap.avatar_find \
										(i.relation, i.account_id, 'medium'), 
				}
		elif category == 'event' :
			for i in EventSnap.event_search(query) :
				yield {
					'data': i, 
					'avatar': AvatarSnap.avatar_all(i.relation, i.account_id), 
				}
		else :
			for i in ClubSnap.club_search(query) :
				yield {
					'data': i, 
					'avatar': AvatarSnap.avatar_all('club', i.id), 
				}

class SquareViews:
	@vary_on_cookie
	def event_all(request) :
		'/square/等的视图'
		dict_render = UserAgentSnap.record(request)
		dict_render['background'] = True
		dict_render['background_color'] = 'f0f0f4'
		dict_render.update(SquareDicts.home_dict_get(request))
		dict_render['title'] = ' - 活动一览'
		return Snap.render('square.html', dict_render)

	@vary_on_cookie
	def club_fetch(request) :
		'/square/club/fetch/ 的视图'
		dict_render = UserAgentSnap.record(request)
		return SquareViews.club_all(request, True)

	@vary_on_cookie
	def club_all(request, fetch=False) :
		'/square/club/ 的视图，通过 ?api=True 返回 json 字符串'
		dict_render = UserAgentSnap.record(request)
		dict_render['background'] = True
		dict_render['background_color'] = '#F0EAE3'
		category = request.GET.get('category', 'all')
		dict_render['category'] = category
		dict_render['link'] = '/square/club/'
		dict_render['category_list'] = ClubSnap.category_list()
		if category == 'all' :
			qry = list(ClubAccount.objects.all())
		else :
			qry = list(ClubAccount.objects.filter(category=category))
		qry.sort(key=SquareSnap.total_rank, reverse=True)
		sliced_qry = AuthDicts.page_dict(request, qry, 6, dict_render)
		dict_render['show_club'] = SquareDicts.club_all \
				(request, sliced_qry, category)
		dict_render['title'] = ' - 社团广场'
		if fetch == False :
			return Snap.render('club_square.html', dict_render)
		else :
			dict_render['title'] = ''
			return Snap.render('club_fetch.html', dict_render)

	@vary_on_headers('User-Agent', 'Cookie')
	def home_view(request) :
		'主页视图'
		n = 0
		dict_render = UserAgentSnap.record(request)
		dict_render['port'] = '@' + request.META['SERVER_PORT']
		dict_render['background'] = True
		dict_render['club_total'] = ClubSnap.club_total()
		dict_render['background_path'] = str(n) + '.png'
		if not 'random selecting pictures' :
			chose = random.choice(tuple(itertools.permutations(range(1, 5), 2)))
			dict_render['background_path'] = '2017-spring/%d%d.png' % chose
	#	dict_render['background_color'] = color_list[n - 1]
		dict_render.update(SquareDicts.home_dict(request))
		dict_render['title'] = ''
		return Snap.render('home.html', dict_render)

	@vary_on_cookie
	def guide_view(request) :
		dict_render = UserAgentSnap.record(request)
		dict_render['title'] = ' - 帮助手册'
		return Snap.render('help.html', dict_render)

	@vary_on_cookie
	def wall_view(request) :
		"[GET] 社团一览（真）"
		dict_render = UserAgentSnap.record(request)
		dict_render.update(SquareDicts.wall())
		dict_render['title'] = ' - 社团名录'
		return Snap.render('wall.html', dict_render)

	@vary_on_cookie
	def search_view(request, category='club') :
		"[GET] 社团搜索"
		dict_render = UserAgentSnap.record(request)
		query = request.GET.get('query', '')
		dict_render['query'] = query
		dict_render['category_cn'], dict_render['btn_color'] = {
			'club': (t_('社团'), 'primary'), 
			'event': (t_('活动'), 'warning'), 
			'share': (t_('分享'), 'success'), 
		}[category]
		dict_render['category'] = category
		dict_render['event_list'] = SquareDicts.home_dict_get_6(request)
		if query :
			dict_render['result'] = SquareDicts.search_dicts(query, category)
		dict_render['title'] = t_(' - %s搜索') % dict_render['category_cn']
		return Snap.render('search.html', dict_render)

	@vary_on_cookie
	@UserAuthority.logged_in
	def note_read(request) :
		dict_render = UserAgentSnap.record(request)
		status = AuthSnap.notice_read(UserSnap.uid_find_by_request(request))
		if status :
			return Snap.success(request, '成功发送反馈')
		else :
			return Snap.success(request, '反馈发送失败')

	@vary_on_cookie
	def club_random(request) :
		'返回随机非三无社团'
		dict_render = UserAgentSnap.record(request)
		club_all = ClubSnap.club_all_find()
		club_filtered = []
		for i in club_all :
			total_rank = SquareSnap.total_rank(i)
			if total_rank :
				club_filtered.append(i)
		if club_filtered :
			club = random.sample(club_filtered, 1)[0]
			return Snap.redirect('/club/%s/' % club.simp_name)
		else :
			raise Http404()


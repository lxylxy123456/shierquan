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

class Snap :
	def success(request, content, update={}) :
		'返回 ajax 的条或者 json 体'
		'''
			特殊指令
				位置		内容			执行
				GET 参数	user-agent	json 化
				HTTP 头	AJAX		json 化
				update	redirect	重定向
		'''
		content = t_(content)
		try :
			request.ua.status_code = 200
			request.ua.save()
		except Exception :
			pass
		if UserAgentSnap.mobile_ua_test(request) \
			or request.META.get('HTTP_AJAX') == 'true' \
			or request.GET.get('Ajax') == 'true' :
			content_dict = { 'status': 'success', 'content': content, }
			content_dict.update(update)
			return HttpResponse(json.dumps(content_dict), 
								content_type="application/json")
		if update.get('redirect') :
			return Snap.redirect(update['redirect'])
		return Snap.render('comp/message.html', {
			'content': content, 
			'prompt': '恭喜', 
		})

	def error(content) :
		'''
			返回一个可以 raise 的 Http403 体，用于要求返回条
			目前已经和 Http403 本身没有区别
		'''
		return Http403(content)

	def redirect(link) :
		'返回 Http302'
		try :
			request = settings.request_thread_safe.request
			request.ua.status_code = 302
			request.ua.save()
		except Exception :
			pass
		return Http302(link)

	def render(template, dict_render) :
		'返回 html 或 json 体'
		request = dict_render.get('request', None)
		try :
			request.ua.status_code = 200
			request.ua.save()
		except Exception :
			pass
		dict_render['title'] = t_(dict_render.get('title', ''))
		if request and UserAgentSnap.mobile_ua_test(request) \
					and request.META.get('HTTP_JSON') == 'true' :
			if not UserAgentSnap.mobile_strict_test(request) :
				raise Snap.error('SECURITY_ERROR: 严格检测失败')
			from django.core.handlers.wsgi import WSGIRequest
			from django.utils.functional import SimpleLazyObject
			from django.contrib.auth.models import AnonymousUser
			dict_items = type({}.items())
			from itertools import starmap
			from quan_account.models import UserAccount
			trans_dict = {
				list:				lambda x: list(map(rec, x)), 
				tuple:				lambda x: list(map(rec, x)), 
				set:				lambda x: list(map(rec, x)), 
				QuerySet:			lambda x: list(map(rec, x)), 
				dict_items:			lambda x: list(map(rec, x)), 
				range:				list, 
				dict:				lambda x: dict(starmap(
										lambda y, z: (y, rec(z)), 
										x.items())), 
				datetime:			lambda x: x.timestamp(), 
				timedelta:			lambda x: x.total_seconds(), 
				WSGIRequest:		lambda x: { 'user': rec(x.user), }, 
				AnonymousUser:		lambda x: None, 
				SimpleLazyObject:	lambda x: rec(x._wrapped),
				str:			lambda x: x, 
			}
			def rec(obj) :
				'输入: 一个任意类型的数据 输出: 可被JSON化的数据'
				obj.__str__()	# 如果删除此行， SimpleLazyObject 的解析会出问题
				if models.Model.__subclasscheck__(type(obj)) :
					try :
						ak = obj.allowed_keys
					except AttributeError :
						ak = ('id', 'first_name', 'last_name')
					# TODO: 在 ak 为空的时候发出警告
					ans = dict(zip(ak, map(lambda x: rec(obj.__dict__[x]), ak)))
					if type(obj) == UserAccount :
						ans['basic'] = rec(ans.basic)
				elif type(obj) in trans_dict :
					ans = trans_dict[type(obj)](obj)
				elif isinstance(obj, collections.Iterable) :
					ans = list(map(rec, obj))
				else :
					ans = obj
				return ans
			
			json_data = json.dumps(rec(dict_render))
			return HttpResponse(json_data, content_type="application/json")
		if 'return-content-type' in dict_render :
			return render_to_response(template, dict_render, 
								content_type=dict_render['return-content-type'])
		else :
			return render_to_response(template, dict_render)

	def file(request, path, name, content_type=None) :
		try :
			request.ua.status_code = 200
			request.ua.save()
		except Exception :
			pass
		# 打开文件
		try :
			file_token = File(open(path, 'rb'))
		except (FileNotFoundError, TypeError) :
			raise Http404('找不到文件')
		# 计算 content_type
		content_type = content_type or mimetypes.guess_type(name)[0] or \
										'application/octet-stream'
		# 计算文件名
		fraw = parse.quote(name)
		uagent = request.META.get('HTTP_USER_AGENT', '')
		if re.search('Trident|Chrome|AppleWebKit', uagent) :
			content_disposition = 'attachment; filename=%s' % fraw
		else :
			content_disposition = "attachment; filename*=\"utf8''%s\"" % fraw
		# 返回
		resp = StreamingHttpResponse(streaming_content=file_token.chunks(), 
									content_type=content_type)
		resp['Content-Disposition'] = content_disposition
		return resp

class ChineseSnap :
	def timedelta_simp(delta) :
		'7300s -> 2小时前'
		#符号，True为以前，False为以后
		signal = delta > timedelta(0)
		signal_word = { True: t_('前'), False: t_('后'), }[signal]
		if not signal :
			delta = timedelta(0) - delta
		if delta.days != 0 :
			return t_('%d天') % delta.days + signal_word
		if delta.seconds // 3600 != 0 :
			return t_('%d小时') % (delta.seconds // 3600) + signal_word
		if delta.seconds // 60 != 0 :
			return t_('%d分钟') % (delta.seconds // 60) + signal_word
		return t_('不到一分钟') + signal_word

	def timedelta_comp(delta) :
		'7300s -> 2小时1分钟'
		sec = delta.total_seconds()
		day = sec // 86400
		if day :
			return t_('%d天') % day
		h = sec // 3600
		m = sec // 60 % 60
		ans = ''
		if h :
			ans += t_('%d小时') % h
		if m :
			ans += t_('%d分钟') % m
		if ans :
			return ans
		else :
			return t_('不到一分钟')

	def byte_exchange(byte_size) :
		'1048576 -> 1.0 MiB'
		if byte_size < 1024**1 :	mod = 1024**0,   'B'
		elif byte_size < 1024**2 :	mod = 1024**1, 'KiB'
		elif byte_size < 1024**3 :	mod = 1024**2, 'MiB'
		elif byte_size < 1024**4 :	mod = 1024**3, 'GiB'
		else :						mod = 1024**4, 'TiB'
		return '%.1f %s' % (byte_size / mod[0], mod[1])

	def datetime_comp(time_set) :
		'返回中文时间，例如 ("9月1日 星期四 ", "08:00")'
		if get_language() == 'en' :
			return (time_set.strftime('%a, %B %d '), 
					time_set.strftime('%H:%M'))
		elif get_language() == 'ja' :
			weekday = '月火水木金土日'[time_set.weekday()]
			return (time_set.strftime('%-m月%-d日 (%%s) ') % weekday, 
					time_set.strftime('%H:%M'))
		weekday = '一二三四五六日'[time_set.weekday()]
		return (time_set.strftime('%-m月%-d日 星期%%s ') % weekday, 
				time_set.strftime('%H:%M'))

	def datetime_simp(time_set) :
		'返回简短时间，例如 ("9月1日 ", "08:00")'
		if get_language() == 'en' :
			return (time_set.strftime('%b %d '), 
					time_set.strftime('%H:%M'))
		elif get_language() == 'ja' :
			return time_set.strftime('%-m月%-d日 '), time_set.strftime('%H:%M')
		return time_set.strftime('%-m月%-d日 '), time_set.strftime('%H:%M')

class UserAgentSnap:
	def record(request) :
		'''
			收取表单头 UserAgent/IP Address统计
			同时 prepare 一下 dict_render ，会包含 request 和 csrf_token
		'''
		settings.request_thread_safe = threading.local()
		settings.request_thread_safe.request = request
		try :
			ipaddr = request.META.get('HTTP_X_FORWARDED_FOR') or \
					request.META.get('REMOTE_ADDR', 'unknown_IP_ADDR')
			ipaddr = ipaddr[0:50]
			try :
				ipaddress.ip_address(ipaddr)
			except ValueError :
				ipaddr = None
			agent = request.META.get('HTTP_USER_AGENT') or \
					request.GET.get('user-agent', 'unknown_AGENT')
			agent = agent[0:100]
			try :
				sname = request.user.last_name
			except AttributeError :
				sname = 'anonymous'
			host = request.META.get('HTTP_HOST', '')
			ua = UserAgentInfo(simp_name=sname, ipaddr=ipaddr, agent=agent, 
					path=request.path, method=request.method, host=host)
			ua.save()
			request.ua = ua
		except Exception :
			logger.error('error in UserAgentSnap.record')
			try :
				logger.error('error path: ' + request.get_full_path())
			except Exception :
				pass
		
		try :
			'CSRF_COOKIE' in request or get_token(request)
		except Exception :
			logger.error('error: failed: get_token(request)')

		dict_render = { 'request': request }
		dict_render.update(csrf(request))
		return dict_render

	def ua_check(request) :
		'''
			访问者是否疑似自动访问器（爬虫）
			日志
				m 在很久以前发现 YisouSpider 等爬虫的存在会让十二圈的某些数据 smd
				l 在 20170130 发现 "Yahoo! Slurp" 是一种爬虫
		'''
		agent = request.META.get('HTTP_USER_AGENT', '')
		return not any(map(lambda x: x in agent, 
							('bot', 'Bot', 'spider', 'Spider', 'Slurp')))

	def examine(request) :
		'检测洪水攻击（已经废弃，因为如果要防御 ddos 的话似乎需要比 Django 底层的技术）'
		'''
			如果两次访问间隔<interval，那么判断为攻击，并对攻击次数计数 返回True
			如果IP地址在IP黑名单中 返回True
			如果攻击记录>3，记录IP黑名单，并将用户账户禁用（如果可用） 返回True
			否则返回False
		'''
		interval = timedelta(0, 1, 0)		# 1秒，攻击间隔界定
		ip = request.META['REMOTE_ADDR']
		user_agent = request.META['HTTP_USER_AGENT']
		if UnwelcomeGuest.objects.filter \
			(ipaddr=UserAgentSnap.ip_get(request)).count() > 0:
			return True
		qry = UnwelcomeGuest.objects.filter(ipaddr=ip)
		sorted_qry = qry.order_by('-time_create')
		time_delta = sorted_qry[1]-sorted_qry[0]
		locked = False		# 是否将要屏蔽这个用户
		if time_delta < interval:
			locked = True
		attack_number = locked
		for index in xrange(2,sorted_qry.count()):		# test index-1 and index
			time_delta = sorted_qry[index]-sorted_qry[index-1]
			if time_delta<interval:
				attack_number+=1
				if attack_number>=3:
					line = UnwelcomeGuest(agent=user_agent,ipaddr=ip)
					line.save()
					return True
		return False

	def name_used(name) :
		'返回真实姓名使用情况'
		return RealNameInfo.objects.filter(name=name, used=0).exists()

	def name_update(name, uid) :
		'使用真实姓名成功注册'
		if name.startswith('t-') :
			status = 'teacher'
		else :
			status = 'student'
		qry = RealNameInfo(name=name, used=0, status=status, account_id=uid)
		qry.save()

	def name_existed(name) :
		'返回真实姓名存在与否'
		return True	# people outside the school can register in shierquan
		# return RealNameInfo.objects.filter(name=name).exists()

	def name_init() :
		'初始化真实姓名数据库'
		BASE_DIR = os.path.dirname(__file__)
		base_path = os.path.join(BASE_DIR, 'data')
		for status in ('student', 'teacher') :
			file_name = status + '_name.txt'
			file_path = os.path.join(base_path, file_name)
			raw = open(file_path, 'rU')
			for ln, line in enumerate(raw):
				if not ln % 100 :
					print('Completed', status, ln)
				rname = line.strip('\n')
				if rname in ('', '\n') :
					break
				if rname[0] == '#' :
					continue
				RealNameInfo(name=rname, status=status).save()
		print('Solving registered users')
		from quan_account.models import UserAccount
		for index, i in enumerate(UserAccount.objects.filter(grade__lte=6)) :
			if not index % 100 :
				print('Completed', index)
			rname = i.basic.first_name
			try :
				qry = RealNameInfo.objects.filter(name=rname, used=0)[0]
			except IndexError :
				print('len(RealNameInfo) < len(User):', rname)
			qry.used = 1
			qry.save()
		print('Done')

	def initialize(fix=0) :
		qry = RealNameInfo.objects.all()
		if fix != 0 :
			qry.delete()
		if qry.count() == 0 :
			UserAgentSnap.name_init()

	def grade_adhere() :
		int('a')
		# 已禁用。除非有人再次犯下了十二圈某原维护者的错误，将年级全部删除了，可删除上一行
		from quan_account.views import UserAccount
		from django.contrib.auth.models import User
		BASE_DIR = os.path.dirname(__file__)
		file_path = os.path.join(BASE_DIR, 'data', "student_grade.txt")
		f = open(file_path, "r")
		grade_dict = {
			'初一': 1, '二四初一': 1, 
			'初二': 2, '二四初二': 2, 
			'初三': 3, '四高一': 3, '国际部初三': 3, 
			'高一': 4, '四高二': 4, '国际部高一': 4, 
			'高二': 5, '四高三': 5, '国际部高二': 5, 
			'高三': 6, '四高四': 6, '国际部高三': 6,
		}
		for line in f :
			name, sgrade = line.split('\t')
			igrade = grade_dict[sgrade[0:-1]]
			qry = User.objects.filter(first_name=name)
			if qry.count() > 0 :
				acc = UserAccount.objects.filter(basic_id=qry[0].id)
				acc.update(grade=igrade)
				print('found ', name)
		#	print(name, igrade)

	def visit_count_by_sname(src, sname) :
		'用户或社团或活动主页的访问量'
		qry = UserAgentInfo.objects.filter(path='/%s/%s/' % (src, sname))
		return qry.count()

	def platform_find(request) :
		'猜测访问者的终端所属平台'
		agent = request.META.get('HTTP_USER_AGENT', 'unknown_AGENT')
		platform_list = ('Windows Phone', 'Android', 'iPhone', 'iPad', 'Mobile')
		return next(filter(lambda x: x in agent, platform_list), 'Web')

	def account_month_calc(src, sname) :
		'对于一个月内的访问情况返回表格[(时间, 次数), (时间, 次数), ...]'
		current = datetime.now()
		qry = UserAgentInfo.objects.filter(path='/%s/%s/' % (src, sname), 
									time_create__gte=current - timedelta(30, 0))
		calc_dict = {}
		for i in range(31) :
			calc_dict[(current - timedelta(i, 0)).date()] = 0
		for i in qry :
			calc_dict[i.time_create.date()] += 1
		calc_list = []
		for i in calc_dict :
			calc_list.append((i, calc_dict[i]))
		return sorted(calc_list, key=lambda x: x[0])

	def login_restrict(request, username) :
		'判断登录尝试是否太频繁'
		# 保存
		agent = request.META.get('HTTP_USER_AGENT')
		if agent is None :
			agent = request.GET.get('user-agent', 'unknown_AGENT')
		agent = agent[0:100]
		password = request.POST.get('password', '') + \
					request.GET.get('password', '')
		password = md5(password.encode()).hexdigest()
		time_now = datetime.now()
		qry = LoginRecord(username=username, agent=agent, 
						password=password, time=time_now)
		qry.save()
		# 判断
		return LoginRecord.objects.filter(username=username, 
				time__gte=time_now-timedelta(0, 60, 0)).count() > 10

	def mobile_ua_test(request) :
		'通过 GET 参数中的 user-agent 判断请求类型'
		translation_dict = {
			'iPhone APP 8649e4100302b57a3dca74a652e7df45': 			'iPhone', 
			'Andriod APP bd4938e2ea804cb5ddaf916813bbd1d7': 		'Andriod', 
			'Windows Phone APP 6e73ae5d3d03b6669fd22c3f525a8fc8': 	'WP', 
			'TMP f029ee24591d136a91abc139f23057b4': 				'tmp', 
		}
		return translation_dict.get(request.GET.get('user-agent', ''), None)

	def mobile_strict_test(request) :
		'''
			增强安全性的hash算法
		'''
		gets = request.GET.dict()
		try :
			sign = gets.pop('sign')
		except KeyError :
			return False
		sort = list(gets.items())
		sort.sort(key=lambda x: list(map(lambda y: y ^ 3**3**3, x[0].encode())))
		plain = '&'.join(map('='.join, sort)) + 'c9a27cb2b3092d0fb345e123475db3'
		hashed = md5(plain.encode()).hexdigest()
		print(hashed, sign)
		return hashed == sign


class UserAgentViews :
	@vary_on_cookie
	def api(request) :
		from quan_square.views import SquareDicts
		dict_render = UserAgentSnap.record(request)
		if request.GET.get('category', '') == 'event' :
			if request.GET.get('time', '') == 'latest' :
				number = 6
				if request.GET.get('number') == '15' :
					number = 15
				event_list = SquareDicts.home_dict_get_6(request, number)
				for i in range(len(event_list)) :
					qry = event_list[i]['data']
					event_list[i]['data'] = {
						'id': qry.id, 
						'subject': qry.subject, 
						'location': qry.location, 
						'content': qry.content, 
					}
				resp = Snap.success(request, '', { 'e': event_list })
				resp['Access-Control-Allow-Origin'] = 'http://hcc.io'
				return resp
		raise Snap.error('参数错误')

	def robots(request) :
		dict_render = UserAgentSnap.record(request)
		name = request.path.rsplit('/', 1)[-1]
		dict_render['return-content-type'] = mimetypes.guess_type(name)[0] or \
										'application/octet-stream'
		if dict_render['return-content-type'] == 'text/xml' :
			dict_render['return-content-type'] = 'application/xml'
		return Snap.render(name, dict_render)


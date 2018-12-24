from .models import *

from quan_account.views import *
from quan_ua.views import *

class EmailSnap :
	def send_mail(server, username, password, sender, reciever, send_show, 
				recv_show, subject, content, subtype='plain', charset='utf-8') :
		'''
			subtype in ('plain', 'html')
		'''
		import smtplib
		from email.mime.text import MIMEText
		srv = smtplib.SMTP()
		srv.connect(server)
		if username and password :
			srv.login(username, password)
		print(datetime.now(), 'log in', sep='\t')
		msg = MIMEText(content, _subtype=subtype, _charset=charset)
		msg['Subject'] = subject
		msg['From'] = send_show
		msg['To'] = ";".join(recv_show)
		srv.sendmail(sender, reciever, msg.as_string())

	def mailto_list_conv(l) :
		'''
			Converts a list of email addresses to addresses with nick names. 
			eg: 	'jkl@hcc.io' -> 'jkl<jkl@hcc.io>'
		'''
		ret = []
		for i in l :
			ret.append('%s<%s>' % (i.split('@')[0], i))
		return ret

	def sendmail(reciever, subject, content, subtype='plain', charset='utf-8') :
		'''
			sending mail for shiyiquan which have less parameters
			including saving to EmailInfo
			仅仅支持发送给一个人(reciever应该写为字符串)
			返回值为("错误信息", 邮件对应EmailInfo)
		'''
		nickname = '=?utf-8?B?%s?=' % \
			base64.b64encode('十一圈'.encode('utf-8')).decode()
		sender = {
			'HCCSERVER': 	lambda x: '"%s" <shiyiquan@shiyiquan.net>' % x, 
			'HCCSERVER-B': 	lambda x: '"%s" <shiyiquan@hcc.io>' % x, 
			'HCCSERVER-C': 	lambda x: '"%s" <shiyiquan@mail.hcc.io>' % x, 
		}.get(socket.gethostname(), lambda x: '')(nickname)
		if EmailInfo.objects.filter(reciever=reciever, time_create__gte=\
			datetime.now()-timedelta(0, 60, 0)).exists() :
			return ('发送频率太高，请在一分钟后重试', None)
		qry = EmailInfo(subject=subject, content=content, sender=sender, 
				reciever=reciever, subtype=subtype, charset=charset)
		if sender == '' :
			print(r'')
			print(r'|| ' * 26)
			print(r'\/ ' * 26)
			print(r'')
			print(r'Subject: %s' % subject)
			print(content)
			print(r'')
			print(r'/\ ' * 26)
			print(r'|| ' * 26)
			print(r'')
		else :
			try :
				EmailSnap.send_mail('127.0.0.1', None, None, sender, [reciever], 
						sender, [reciever], subject, content, subtype, charset)
			except Exception as e :
				qry.status = repr(e)
				qry.save()
				return ('邮件服务器错误', qry)
		qry.save()
		return (None, qry)

	def reciever_list_generate(reciever) :
		'''
			reciever
				head	所有社长
				all		所有人
		'''
		if reciever == 'head' :
			user_list = AccountRelation.objects.filter \
						(relation='head').values_list('account_id_A', flat=True)
			return User.objects.filter(id__in=user_list)
		elif reciever == 'all' :
			return User.objects.filter()
		return []

class EmailViews :
	@never_cache
	def password_reset(request) :
		'/reset/	重置密码'
		def generate_code() :
			raw = repr(datetime.now()) + str(random.randrange(1000000000000000))
			return md5(raw.encode()).hexdigest()
		dict_render = UserAgentSnap.record(request)
		if UserSnap.uid_find_by_request(request) :
			return Snap.redirect('/user/')
		if request.method == 'POST' :
			first_name = request.POST.get('first_name', '')
			username = request.POST.get('username', '')
			qry = User.objects.filter(first_name=first_name)
			print(first_name)
			if not qry :
				raise Snap.error('此用户尚未注册，请尝试注册')
			qry2 = qry.filter(username=username)
			if not qry2 :
				email_list = []
				for i in qry :
					email = i.username.split('@')
					email_list.append(email[0][:3] + '***' + '@' + email[1])
				raise Snap.error(t_('请输入正确的邮箱，可能是 %s') % \
											(t_(' 或 ').join(email_list)))
			code = generate_code()
			while EmailInfo.objects.filter(data=code, \
				category__in=('password-reset', 'password-reset-used')) :
				generate_code()
			image = ''
			content = get_template('email/password_reset_email.html').render \
				({ 'code': code, 'image': image })
			result = EmailSnap.sendmail(username, '十一圈密码重置链接', 
										content, subtype='html')
			if result[1] :
				result[1].account_id = qry2[0].id
				result[1].relation = 'user'
				result[1].data = code
				result[1].category = 'password-reset'
				result[1].save()
			if result[0] :
				raise Snap.error(result[0])
			return Snap.success(request, '邮件已经发送，请查收', 
								{ 'redirect': '/login/' })
		dict_render['title'] = ' - 找回密码'
		return Snap.render('password_reset.html', dict_render)

	@never_cache
	def password_set(request, code) :
		'/reset/{{ code }}/	重置密码'
		dict_render = UserAgentSnap.record(request)
		try :
			qry = EmailInfo.objects.get(data=code, \
					category__in=('password-reset', 'password-reset-used'))
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			raise Http404('验证码无效')
		if qry.time_create < datetime.now() - timedelta(1, 0, 0) :
			raise Http404('验证码已经过期，请尝试重新生成')
		if qry.category == 'password-reset-used' :
			raise Http404('验证码已使用，请重新生成')
		if request.method == 'POST' :
			password = request.POST.get('password')
			if not password :
				raise Snap.error('请输入密码')
			user = UserSnap.user_find_by_uid(qry.account_id)
			user.set_password(password)
			user.save()
			qry.category = 'password-reset-used'
			qry.save()
			return Snap.success(request, '成功更改密码', 
								{ 'redirect': '/login/' })
		user = UserSnap.user_find_by_uid(qry.account_id)
		dict_render['username'] = user.username
		dict_render['first_name'] = user.first_name
		dict_render['code'] = code
		dict_render['title'] = ' - 密码重置'
		return Snap.render('password_set.html', dict_render)

	def global_email(request) :
		'群发邮件'
		dict_render = UserAgentSnap.record(request)
		raise Http403()
		if request.method == 'GET' :
			dict_render['title'] = ' - 邮件群发'
			return Snap.render('global_email.html', dict_render)
		recv_data = json.loads(request.POST['data'])
		subject = recv_data['subject']
		content = recv_data['content']
		reciever = recv_data['reciever']
		subtype = recv_data['subtype']
		if subtype not in ('html', 'plain') :
			raise Snap.error('subtype 不正确')
		if not subject or not content :
			raise Snap.error('内容不全')
		if reciever not in ('all', 'head') :
			raise Snap.error('收信人不正确')
		reciever_list = EmailSnap.reciever_list_generate(reciever)
		result_list = []
		for i in reciever_list :
			result = EmailSnap.sendmail(i.username, subject, 
										content, subtype=subtype)
			result_list.append((i.first_name, i.username, result[0]))
		return Snap.success(request, '发送成功', { 'result_list': result_list })


from .models import *

from quan_account.models import *

from quan_account.views import *
from quan_ua.views import *

class MobileSnap :
	def uid_find_by_host_id(hid) :
		'host_id->uid'
		qry = MobileHost.objects.filter(host_id=hid).order_by('-time_create')
		try :
			return qry[0].account_id
		except IndexError :
			return 0

	def club_information_find(uid) :
		'''
			[JSON] 返回用户的社团列表，包括
			fname, sname, status in ['head', 'member', 'vice', 'follower']
		'''
		qry = AccountRelation.objects.filter(account_id_A=uid, 
			relation__in = ['head', 'member', 'vice', 'follower'])
		club_list = []
		for i in ClubSnap.club_find_by_uid(uid, True) :		# 成员
			club_list.append({
				'id': i.id, 
				'sname': i.simp_name, 
				'fname': i.full_name, 
				'status': ClubSnap.club_position_by_uid(i.id, uid), 
			})
		for i in ClubSnap.club_find_by_uid(uid, False) :	# 关注
			club_list.append({
				'id': i.id, 
				'sname': i.simp_name, 
				'fname': i.full_name, 
				'status': ('follower', '关注者'), 
			})
		return club_list

class MobileViews :
	@vary_on_cookie
	def host_id_save(request) :
		'''
			输入:[GET]		host_id=[host id]
			输出:[SESSION]	host_id=[host id]
		'''
		dict_render = UserAgentSnap.record(request)
		hid = request.GET.get('host_id', '')
		request.session['host_id'] = hid
		if not hid :
			raise Snap.error('对象没有被指定')
		try :
			uid = int(UserSnap.uid_find_by_request(request))
		except Exception :
			uid = 0
		if not MobileHost.objects.filter(host_id=hid).update(account_id=uid) :
			MobileHost(host_id=hid, account_id=uid).save()
		return Snap.success(request, hid)

	@vary_on_cookie
	def clublist_find(request) :
		'''
			输入:[GET]	host_id=[host id]
			输出:[JSON]	{ club_list: 社团列表 }，包括
				fname, sname, status in ['head', 'member', 'vice', 'follower']
				如果错误，返回的 club_list 是空列表
		'''
		dict_render = UserAgentSnap.record(request)
		hid = request.GET.get('host_id', '')
		if not hid :
			raise Snap.error('找不到对象')
		uid = MobileSnap.uid_find_by_host_id(hid)
		club_list = MobileSnap.club_information_find(uid)
		return Snap.success(request, '', { 'club_list': club_list })

	@vary_on_cookie
	def host_id_find(request) :
		'[string] 得到可用的hostid'
		dict_render = UserAgentSnap.record(request)
		for i in range(10) :
			uuid.uuid1()
		while 1 :
			hid = str(uuid.uuid1())
			if not MobileSnap.uid_find_by_host_id(hid) :
				return Snap.success(request, hid)

	@vary_on_cookie
	def privacy(request) :
		'显示隐私政策'
		dict_render = UserAgentSnap.record(request)
		content = ('为了确保十一圈客户端正常工作，此应用必须向服务器传输一些数据，'
					'例如登录的用户名和密码。我们不会传输您的任何私人数据。')
		if request.GET.get('client', '') :
			return Snap.success(request, content)
		else :
			dict_render['content'] = content
			dict_render['title'] = ' - 隐私政策'
			return Snap.render('privacy_policy.html', dict_render)


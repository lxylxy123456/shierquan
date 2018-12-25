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

from quan_center.models import *
from quan_forum.models import *
from quan_message.models import *

from quan_message.views import PublicMessageAction, PrivateMessageAction
from quan_ua.views import *

class UserAuthority :
	def club_union_check(view_func) :
		'''
			源代码自 django.contrib.auth.decorators.user_passes_test
			使用: @UserAuthority.club_union_check
		'''
		from functools import wraps
		from django.utils.decorators import available_attrs
		@wraps(view_func, assigned=available_attrs(view_func))
		def _wrapped_view(request, *args, **kwargs):
			if AccountRelation.objects.filter(
				account_id_A=request.user.id, 
				account_id_B=ClubSnap.cid_find_by_sname('club-union'), 
				relation__in=('core', 'vice', 'head')).exists() :
				return view_func(request, *args, **kwargs)
			UserAgentSnap.record(request)
			raise Http403('如果为社联成员，请检查登录情况。')
		return _wrapped_view

	def club_president(sname, relation=('head', )) :
		'''
			源代码自 django.contrib.auth.decorators.user_passes_test
			使用: @UserAuthority.club_president('hcc-computer-community')
		'''
		from functools import wraps
		from django.utils.decorators import available_attrs
		def decorator(view_func):
			@wraps(view_func, assigned=available_attrs(view_func))
			def _wrapped_view(request, *args, **kwargs):
				if AccountRelation.objects.filter(
					account_id_A=request.user.id, 
					account_id_B=ClubSnap.cid_find_by_sname(sname), 
					relation__in=relation).exists() :
					return view_func(request, *args, **kwargs)
				UserAgentSnap.record(request)
				raise Http403('您没有社团管理权限')
			return _wrapped_view
		return decorator
	
	def assert_permission(request, src, aid, vice=False, core=False):
		if not aid or not AccountSnap.aid_verify(request, src, aid, vice, core):
			raise Http403('您没有社团管理权限')

	def logged_in(view_func) :
		'''
			源代码自 django.contrib.auth.decorators.user_passes_test
			# /usr/lib/python3.5/site-packages/django/contrib/auth/decorators.py
			使用: @UserAuthority.logged_in
		'''
		from functools import wraps
		from django.utils.decorators import available_attrs
		@wraps(view_func, assigned=available_attrs(view_func))
		def _wrapped_view(request, *args, **kwargs):
			if request.user.is_authenticated() :
				return view_func(request, *args, **kwargs)
			UserAgentSnap.record(request)
			if request.META.get('HTTP_AJAX') == 'true' :
				raise Http403('请登录十二圈后再进行操作')
			else :
				url = parse.quote(request.get_full_path())
				return Snap.redirect('/login/?url=%s' % url)
				# 没有包含原来的路由，可以用原来的代码扩充
		return _wrapped_view

class UserSnap:
	def account_find_by_request(request) :
		'获取已登录用户'
		try :
			return UserAccount.objects.get(basic_id=request.user.id)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def uid_find_by_request(request) :
		'获取已登录用户ID'
		return request.user.id 

	def sname_find_by_request(request) :
		'获取已登录用户简称'
		if request.user.is_authenticated() :
			return request.user.last_name
		else :
			return None

	def fname_find_by_request(request) :
		'获取已登录用户全称'
		if request.user.is_authenticated() :
			return request.user.first_name
		else :
			return None
			
	def sname_find_by_uid(uid) :
		'通过id得到用户简称'
		cache_key = 'UserSnap__sname_find_by_uid__%d' % uid
		cached = cache.get(cache_key)
		if cached :
			return cached
		try :
			answer = User.objects.get(id=uid).last_name
			cache.set(cache_key, answer, random.randint(800000, 900000))
			return answer
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def fname_find_by_uid(uid) :
		'通过id得到用户全称'
		cache_key = 'UserSnap__fname_find_by_uid__%d' % uid
		cached = cache.get(cache_key)
		if cached :
			return cached
		try :
			answer = User.objects.get(id=uid).first_name
			cache.set(cache_key, answer, random.randint(800000, 900000))
			return answer
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def sname_validate(sname) :
		'验证last_name是否有效'
		m = re.match('([a-zA-Z\-]+)$', sname)
		if m == 'anonymous' :
			raise Snap.error('昵称已被保留，无法注册')
		if not m :
			raise Snap.error('请使用小写字母和连线符组合链接 如：test-user')
		if User.objects.filter(last_name__in=(sname, sname.lower())).exists() :
			raise Snap.error('昵称已被注册')

	def grade_find_by_uid(uid, chinese=False) :
		'通过uid获取年级'
		try :
			grade = UserAccount.objects.get(basic_id=uid).grade
			if chinese :
				return UserSnap.grade_translate(grade)
			else :
				return grade
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def grade_translate(grade) :
		if get_language() == 'en' :
			return ('Alien', 'Grade 7', 'Grade 8', 'Grade 9', 
						'Grade 10', 'Grade 11', 'Grade 12', 'Graduate')[grade]
		elif get_language() == 'ja' :
			return ('宇宙人', '中一', '中二', '中三', 
						'高一', '高二', '高三', '卒業')[grade]
		return ('外星人', '初一', '初二', '初三', 
						'高一', '高二', '高三', '荣誉成员')[grade]

	def uid_find_by_sname(sname) :
		try :
			return User.objects.get(last_name=sname).id
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None
		
	def uid_find_by_fname(fname) :
		try :
			return User.objects.get(first_name=fname).id
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def user_find_by_uid(uid) :
		try :
			return User.objects.get(id=uid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def account_find_by_uid(uid) :
		try :
			return UserAccount.objects.get(basic_id=uid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def signature_modify(uid, sign) :
		'修改用户签名，返回是否成功'
		try :
			qry = UserAccount.objects.get(basic_id=uid)
			qry.signature = sign
			qry.save()
			return True
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return False

	def nickname_find_by_uid(uid) :
		'如果没有写，返回sname'
		cache_key = 'UserSnap__nickname_find_by_uid__%d' % uid
		cached = cache.get(cache_key)
		if cached :
			return cached
		try :
			qry = UserAccount.objects.get(basic_id=uid)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return ''
		answer = qry.nickname or qry.basic.last_name
		cache.set(cache_key, answer, random.randint(800000, 900000))
		return answer

	def nickname_set(uid, nickname) :
		'返回是否成功'
		try :
			qry = UserAccount.objects.get(basic_id=uid)
			qry.nickname = nickname
			qry.save()
			return True
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return False

	def signature_find_by_uid(uid) :
		'如果没有写，返回sname'
		try :
			return UserAccount.objects.get(basic_id=uid).signature
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return ''

	def email_validate(email) :
		'验证邮箱地址 如果符合格式返回True'
		ptn = r"^([a-zA-Z0-9_-_.])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+"
		if re.match(ptn, email) :
			return True
		else :
			return False

	def is_friend(ida, idb) :
		return AccountRelation.objects.filter(
						Q(account_id_A=ida, account_id_B=idb) | 
						Q(account_id_A=idb, account_id_B=ida), 
						relation='uu-friend').exists()

	def friend_status_find(ida, idb) :
		'''
			none					没有关系
			friend					朋友
			friend-waiting			a等待b
			friend-waiting-reverse	b等待a
		'''
		if UserSnap.is_friend(ida, idb) :
			return 'friend'
		qry = AccountRelation.objects.filter(relation='uu-friend-wait')
		if qry.filter(account_id_A=ida, account_id_B=idb).exists() :
			return 'friend-waiting-reverse'
		if qry.filter(account_id_A=idb, account_id_B=ida).exists() :
			return 'friend-waiting'
		return 'none'

	def is_follower(host_id, follower_id) :
		'follower关注host'
		return AccountRelation.objects.filter(relation='uu-follower', 
						account_id_A=follower_id, account_id_B=host_id).exists()

	def is_contact(host_id, follower_id) :
		'follower关注host 或者 是朋友'
		return UserSnap.is_follower(host_id, follower_id) or \
				UserSnap.is_friend(host_id, follower_id)

	def is_friend_annoy(ida, idb) :
		'是否扰民'
		return AccountRelation.objects.filter(relation='uu-friend-deny', 
						account_id_A=ida, account_id_B=idb).count() >= 3

	def friend_wait(ida, idb) :
		AccountRelation \
			(account_id_A=ida, account_id_B=idb, relation='uu-friend-wait') \
			.save()

	def friend_check(ida, idb) :
		AccountRelation.objects.filter \
			(account_id_A=ida, account_id_B=idb, relation='uu-friend-wait') \
			.update(relation='uu-friend')
		AccountRelation.objects.filter \
			(account_id_A=idb, account_id_B=ida, relation='uu-friend-wait') \
			.update(relation='uu-friend')

	def friend_break(ida, idb) :
		AccountRelation.objects.filter \
			(account_id_A=ida, account_id_B=idb, relation__in= \
			('uu-friend', 'uu-friend-wait')).update(relation='uu-friend-break')
		AccountRelation.objects.filter \
			(account_id_A=idb, account_id_B=ida, relation__in= \
			('uu-friend', 'uu-friend-wait')).update(relation='uu-friend-break')

	def friend_deny(ida, idb) :
		AccountRelation.objects.filter \
			(account_id_A=ida, account_id_B=idb, relation__in= \
			('uu-friend', 'uu-friend-wait')).update(relation='uu-friend-deny')
		AccountRelation.objects.filter \
			(account_id_A=idb, account_id_B=ida, relation__in= \
			('uu-friend', 'uu-friend-wait')).update(relation='uu-friend-deny')

	def follow(host_id, follower_id) :
		if AccountRelation.objects.filter(account_id_A=follower_id, 
			account_id_B=host_id, relation='uu-follower').count() == 0 :
			AccountRelation (account_id_A=follower_id, account_id_B=host_id, 
				relation='uu-follower').save()

	def follow_break(host_id, follower_id) :
		print(host_id, follower_id)
		AccountRelation.objects.filter \
			(account_id_A=follower_id, account_id_B=host_id, relation= \
			'uu-follower').update(relation='uu-follower-break')

	def contact_list(uid) :
		'返回uid组成的list ，联系人集合等于好友集合'
		return set(itertools.chain(
			AccountRelation.objects.filter(account_id_A=uid, 
				relation='uu-friend').values_list('account_id_B', flat=True), 
			AccountRelation.objects.filter(account_id_B=uid, 
				relation='uu-friend').values_list('account_id_A', flat=True), 
		))

	def following_find(uid) :
		'被关注用户ID列表'
		return AccountRelation.objects.filter(account_id_A=uid, 
				relation="uu-follower").values_list('account_id_B', flat=True)

	def user_search(query) :
		'搜索用户，返回 User 的 yield 体'
		searched_id = set()
		for i in UserAccount.objects.filter(nickname=query).iterator() :
			if i.basic.id not in searched_id :
				yield i.basic; searched_id.add(i.basic.id)
		for i in User.objects.filter(Q(last_name=query) | Q(first_name=query)) \
																.iterator() :
			if i.id not in searched_id :
				yield i; searched_id.add(i.id)
		for i in UserAccount.objects.filter(nickname__icontains=query) \
																.iterator() :
			if i.basic.id not in searched_id :
				yield i.basic; searched_id.add(i.basic.id)
		for i in UserAccount.objects.filter(pinyin__icontains=query) \
																.iterator() :
			if i.basic.id not in searched_id :
				yield i.basic; searched_id.add(i.basic.id)

	def person_info(fname) :
		'''
			得到用户信息
			[危险] 这个功能可能导致严重的用户数据泄漏，因此不应该在非 shell 环境使用
		'''
		qry = UserAccount.objects.get \
			(basic_id=UserSnap.uid_find_by_fname(fname))
		print('user_id =', repr(qry.basic.id), sep='\t')
		print('UAccount_id =', repr(qry.id), sep='\t')
		print('username =', repr(qry.basic.username), sep='\t')
#		print('password =', repr(qry.basic.password), sep='\t')
		print('first_name =', repr(qry.basic.first_name), sep='\t')
		print('last_name =', repr(qry.basic.last_name), sep='\t')
		print('phone =', '', repr(qry.phone), sep='\t')
		print('grade =', '', qry.grade, sep='\t')
		print('nickname =', repr(qry.nickname), sep='\t')
		print('signature =', repr(qry.signature), sep='\t')
		print('pinyin =', repr(qry.pinyin), sep='\t')

class ClubSnap:
	def sname_verify(request, sname, vice=False, core=False) :
		'通过社团简称验证社长身份，认为 vice >= core'
		try :
			cid = ClubSnap.cid_find_by_sname(sname)
		except Http404 :
			return False
		return ClubSnap.cid_verify(request, cid, vice, core)

	def cid_verify(request, cid, vice=False, core=False) :
		'通过社团ID验证社长身份，认为 vice >= core'
		if not request.user.is_authenticated() :
			return False
		uid = request.user.id
		if not vice :
			return AccountRelation.objects.filter(account_id_A=uid, 
					account_id_B=cid, relation='head').exists()
		elif not core :
			return AccountRelation.objects.filter(account_id_A=uid, 
					account_id_B=cid, relation__in=('head', 'vice')).exists()
		else :
			return AccountRelation.objects.filter(account_id_A=uid, 
					account_id_B=cid, relation__in=('head', 'vice', 'core')) \
																	.exists()

	def club_find_by_sname(sname) :
		'获取社团'
		try :
			return ClubAccount.objects.get(simp_name=sname)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def fname_find_by_cid(cid) :
		'获取社团全称'
		cache_key = 'ClubSnap__fname_find_by_cid__%d' % cid
		cached = cache.get(cache_key)
		if cached :
			return cached
		try :
			answer = ClubAccount.objects.get(id=cid).full_name
			cache.set(cache_key, answer, random.randint(800000, 900000))
			return answer
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def create(uid, nclub) :
		'创建社长并返回'
		nrel = AccountRelation(account_id_A=uid, account_id_B=nclub.id, 
								relation="head")
		nrel.save()
		return nrel

	def sname_find_by_cid(cid) :
		'社团ID => 社团简短名称'
		cache_key = 'ClubSnap__sname_find_by_cid__%d' % cid
		cached = cache.get(cache_key)
		if cached :
			return cached
		try :
			answer = ClubAccount.objects.get(id=cid).simp_name
			cache.set(cache_key, answer, random.randint(800000, 900000))
			return answer
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def sname_validate(sname) :
		'验证simp_name是否有效'
		if not re.match('([a-zA-Z\-]+$)', sname) :
			raise Snap.error('请使用小写字母和连线符组合链接 如：test-club')
		t = (sname, sname.lower())
		if ClubAccount.objects.filter(simp_name__in=t).exists() :
			raise Snap.error('社团名称已被注册')
		if ClubAlias.objects.filter(alias__in=t).exists() :
			raise Snap.error('社团名称已被注册')

	def cid_find_by_sname(sname) :
		'社团简短名称 => 社团ID'
		try :
			return ClubAccount.objects.get(simp_name=sname).id
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			try :
				return ClubAlias.objects.get(alias=sname, status=0).club_id
			except (ObjectDoesNotExist, MultipleObjectsReturned) :
				raise Http404

	def join(cid, request) :
		'加入(return True)或者退出(return False)'
		nclub = ClubAccount.objects.filter(id=cid)
		ouser = AccountRelation.objects.filter(account_id_A=request.user.id, 
					account_id_B=cid, relation__in=('member', 'vice', 'head', 
					'core', 'member-wait'))
		if not ouser.exists() and nclub.exists() :
			nrel = AccountRelation(account_id_A=request.user.id, 
					account_id_B=nclub[0].id, relation="member-wait")
			nrel.save()
			return True
		else :
			if ouser.filter(relation='head').exists() :
				raise Snap.error('社长不可以退出社团')
			ouser.delete()
			return False

	def follow(cid, request) :
		'关注（return True）或取消关注（return False）'
		nclub = ClubAccount.objects.filter(id=cid)
		ouser = AccountRelation.objects.filter(account_id_A=request.user.id, 
					account_id_B=cid, relation="follower")
		if not ouser.exists() and nclub.exists() :
			fo = AccountRelation(account_id_A=request.user.id, 
					account_id_B=nclub[0].id, relation="follower")
			fo.save()
			return True
		else :
			ouser.delete()
			return False

	def club_followed_by_uid(uid, cid) :
		'是否已经跟随'
		return AccountRelation.objects.filter(account_id_B=cid, 
						relation="follower", account_id_A=uid).exists()

	def club_joined_by_uid(uid, cid) :
		'证明用户加入社团的数据库字段'
		return AccountRelation.objects.filter(account_id_B=cid, 
				relation__in=('head', 'vice', 'core', 'member', 'member-wait'), 
				account_id_A=uid)

	def club_position_by_uid(cid, uid) :
		'''
			5		4		3		2		1			0
			head	vice	core	member	member-wait	none
			社长		副社长	核心社员	普通社员	等待审核		不是成员
		'''
		qry = ClubSnap.club_joined_by_uid(uid, cid).values_list \
														('relation', flat=True)
		level_dict = {
			'member-wait': 1, 'member': 2, 'core': 3, 'vice': 4, 'head': 5, 
		}
		level = max(map(lambda x: level_dict.get(x, 0), qry), default=0)
		if get_language() == 'en' :
			return {
				0: ('none', 'Nonmember'), 
				1: ('member-wait', 'Waiting for Verification'), 
				2: ('member', 'Member'), 
				3: ('core', 'Core Member'), 
				4: ('vice', 'Vice President'), 
				5: ('head', 'President'), 
			}[level]
		elif get_language() == 'ja' :
			return {
				0: ('none', '関係なし'), 
				1: ('member-wait', '偽部員'), 
				2: ('member', '部員'), 
				3: ('core', 'コア部員'), 
				4: ('vice', '副部長'), 
				5: ('head', '部長'), 
			}[level]
		return {
			0: ('none', '不是成员'), 
			1: ('member-wait', '等待审核'), 
			2: ('member', '普通社员'), 
			3: ('core', '核心社员'), 
			4: ('vice', '副社长'), 
			5: ('head', '社长'), 
		}[level]

	def follower_total(cid) :
		'关注用户总数'
		return AccountRelation.objects.filter(account_id_B=cid, 
				relation="follower").count()

	def follower_find(cid) :
		'关注用户qry'
		return AccountRelation.objects.filter(account_id_B=cid, 
				relation="follower")

	def follower_list(cid, return_type='nickname') :
		'return_type in (nickname, id) ，返回 map 生成器'
		qry = ClubSnap.follower_find(cid).values_list('account_id_A', flat=True)
		if return_type == 'nickname' :
			return map(UserSnap.nickname_find_by_uid, qry)
		elif return_type == 'id' :
			return map(int, qry)
		else :
			return map(int, [])

	def member_total(cid) :
		'社员总数'
		return len(ClubSnap.member_all(cid))

	def member_all(cid) :
		'所有社团成员的 uid 列表'
		return set(AccountRelation.objects.filter(account_id_B=cid, 
				relation__in=('member', 'vice', 'head', 'core')).values_list \
													('account_id_A', flat=True))

	def grade_list_by_cid(cid) :
		'成员的年级列表，会重复年级，不会重复成员'
		return map(UserSnap.grade_find_by_uid, ClubSnap.member_all(cid))

	def attendence_total(uid, cid) :
		'获得用户加入社团的时间长'
		qry = AccountRelation.objects.filter(account_id_A=uid, 
			account_id_B=cid, relation__in=('member', 'vice', 'head', 'core')) \
			.values_list('time_create', flat=True)
		now = datetime.now()
		return now - min(qry, default=now)

	def head_find_by_cid(cid) :
		'获取社长'
		try :
			rel = AccountRelation.objects.get(account_id_B=cid, relation="head")
			return User.objects.get(id=rel.account_id_A)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def head_id_find_by_cid(cid) :
		'获取社长ID'
		try :
			rel = AccountRelation.objects.get(account_id_B=cid, relation="head")
			return rel.account_id_A
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def head_sname_find_by_cid(cid) :
		'获取社长简称'
		try :
			rel = AccountRelation.objects.get(account_id_B=cid, relation="head")
			return User.objects.get(id=rel.account_id_A).last_name
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def vice_find_by_cid(cid) :
		'获取副社长'
		try :
			rel = AccountRelation.objects.get(account_id_B=cid, relation="vice")
			return User.objects.get(id=rel.account_id_A)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def leader_find_by_cid(cid) :
		'返回[社长, 副社长]（类型为User对象）'
		qry = (ClubSnap.head_find_by_cid(cid), ClubSnap.vice_find_by_cid(cid))
		return list(filter(bool, qry))

	def head_change(cid, fname, force=False) :
		'更换社长，fname为将要变更的人'
		if fname == None :
			raise Snap.error('没有输入任何姓名')
		uid = UserSnap.uid_find_by_fname(fname)
		if uid == None :
			raise Snap.error('社团的新社长尚未在十二圈落户')
		qry_new = AccountRelation.objects.filter(account_id_A=uid, 
				account_id_B=cid, relation__in=('member', 'vice'))
		qry_old = AccountRelation.objects.filter(account_id_B=cid, 
				relation='head')
		if not qry_old.exists() :
			raise Snap.error('数据错误')
		elif uid == qry_old[0].account_id_A :
			raise Snap.error('将社团新社长指派给原社长')
		if not qry_new.exists() :
			if not force :
				raise Snap.error('给别的社团的人？')
			qry_old.update(relation='member')
			qry_new = AccountRelation(account_id_A=uid, 
					account_id_B=cid, relation='head')
			qry_new.save()
			return 'Warning: forced to do so'
		qry_old.update(relation='member')
		qry_new.update(relation='head')
		return True

	def vice_change(cid, fname) :
		'更换副社长，fname为将要变更的人'
		if fname == None :
			raise Snap.error('没有输入任何姓名')
		uid = UserSnap.uid_find_by_fname(fname)
		if uid == None :
			raise Snap.error('指派的副社长尚未在十二圈落户')
		qry_new = AccountRelation.objects.filter(account_id_A=uid, 
				account_id_B=cid, relation='member')
		qry_old = AccountRelation.objects.filter(account_id_B=cid, 
				relation='vice')
		if qry_old.exists() and uid == qry_old[0].account_id_A :
			raise Snap.error('副社长已被指派')
		if not qry_new.exists() :
			raise Snap.error('副社长非本社团成员')
		qry_old.update(relation='member')
		qry_new.update(relation='vice')
		return True

	def wait_reject(cid, uid) :
		'拒绝社员请求，返回是否成功'
		qry = AccountRelation.objects.filter(relation='member-wait', 
			account_id_A=uid, account_id_B=cid).update \
				(relation='member-wait-deny')
		return True

	def wait_member(cid, uid) :
		'同意社员请求，返回是否成功'
		qry = AccountRelation.objects.filter(relation='member-wait', 
			account_id_A=uid, account_id_B=cid).update(relation='member')
		return True

	def member_remove(cid, uid) :
		'删除社员，返回是否成功'
		qry = AccountRelation.objects.filter(account_id_A=uid, 
			account_id_B=cid, relation__in=('member', 'vice', 'core')).update \
				(relation='member-break')
		return True

	def member_core(cid, uid) :
		"转换社员是否核心，返回变换以后是否是核心"
		qry = AccountRelation.objects.filter(account_id_A=uid, relation="core", 
											account_id_B=cid)
		if not qry.exists() :
			AccountRelation(account_id_A=uid, account_id_B=cid, 
				relation="core").save()
			return True
		else :
			qry.delete()
			return False

	def member_wait_find(cid) :
		'得到社团中的所有待通过申请'
		return AccountRelation.objects.filter(account_id_B=cid, 
			relation='member-wait')

	def club_union_check(request) :
		'检查用户是否是社联成员'
		uid = UserSnap.uid_find_by_request(request)
		cid = ClubSnap.cid_find_by_sname('club-union')
		return AccountRelation.objects.filter(account_id_A=uid, 
			account_id_B=cid, relation__in=('core', 'vice', 'head')).exists()

	def club_remove(cid) :
		'删除社团，返回True'
		assert not '太危险，已经被禁用'
		from quan_event.models import EventInfo, EventRelation, EventQuest
		from quan_share.models import ShareInfo, ShareAttach
		from quan_avatar.models import AvatarAccount
		from quan_badge.models import BadgeInfo, BadgeRelation, TagInfo
		from quan_auth.models import AuthInfo
		from quan_message.views import MessageSnap
		ClubAccount.objects.filter(id=cid).delete()
		AccountRelation.objects.filter(relation__in=('head', 'vice', 'core', 
				'member', 'member_wait', 'follower', 'cc-friend', 'qrank'), 
				account_id_B=cid).delete()
		AccountRelation.objects.filter(relation='cc-friend', 
				account_id_A=cid).delete()
		# share
		share_qry = ShareInfo.objects.filter(relation='club', account_id=cid)
		for i in share_qry :
			MessageSnap.message_delete('share', i.id)
		share_qry.update(status=1)
		ShareAttach.objects.filter(relation='club', account_id=cid).delete()
		# event
		event_qry = EventInfo.objects.filter(relation='club', account_id=cid)
		event_id = []
		for i in event_qry :
			MessageSnap.message_delete('event', i.id)
			event_id.append(i.id)
		event_qry.update(category='deleted')
		EventRelation.objects.filter(event_id__in=event_id).delete()
		EventQuest.objects.filter(event_id__in=event_id).delete()
		# avatar
		AvatarAccount.objects.filter(relation='club', account_id=cid).delete()
		# badge
		badge_qry = BadgeInfo.objects.filter(relation='club', account_id=cid)
		badge_id_list = []
		for i in badge_qry :
			MessageSnap.message_delete('badge', i.id)
			badge_id_list.append(i.id)
		badge_qry.delete()
		BadgeRelation.objects.filter(badge_id__in=badge_id_list).delete()
		# tag (in quan_badge/models.py)
		TagInfo.objects.filter(relation='club', account_id=cid).delete()
		# auth
		AuthInfo.objects.filter(relation='club', account_id=cid).delete()
		# message
		MessageSnap.message_delete('club', cid)
		# alias
		ClubAlias.objects.filter(club_id=cid, status=0).update(status=1)
		return True

	def club_total() :
		'返回当前社团总数'
		return ClubAccount.objects.count()

	def intro_truncate() :
		assert not '已禁用'
		qry = ClubAccount.objects.all()
		for club in qry :
			club.simp_intro = club.full_intro[0:60]
			print(club.simp_intro)
			club.save()

	def club_search(query) :
		'根据社长或副社长的全名精确搜索，或者根据社团字段搜索。返回 ClubAccount 数据库列表'
		id_set = set()
		for i in User.objects.filter(first_name=query).iterator() :
			id_set.update(AccountRelation.objects.filter \
				(account_id_A=i.id, relation__in=('head', 'vice')).values_list \
													('account_id_B', flat=True))
		return ClubAccount.objects.filter(Q(id__in=id_set) | 
				Q(simp_name__icontains=query) | Q(full_intro__icontains=query)|
				Q(full_name__icontains=query) | Q(simp_intro__icontains=query))

	def category_list() :
		'''
			返回社团联盟列表
			最好将这里的更新同步到: http://zh.hcc.wikia.com/wiki/十二圈/社团联盟列表
		'''
		if get_language() == 'en' :
			return [
				('interest', 'Animation'), 			# 动漫同好
				('technology', 'Information Technology'), 
				('media', 'Media'), 
				('sport', 'Sports'), 				# 体育运动
				('art', 'Art'), 					# 艺术表演 + 艺术设计
				('campus', 'Campus Management'), 
				('charity', 'Charity'), 			# 慈善公益
				('nature-sci', 'Natural Science'), 
				('social-sci', 'Social Science'), 
				('business', 'Business'), 			# 商业经营
				('stage', 'Stage Design'), 
				('manufacture', 'Manufacture'), 	# 手工制作
				('publishment', 'Publishment'), 	# 文学出版
				('language', 'Languages'), 			# 语言学习
				('other', 'Other'), 
			]
		elif get_language() == 'ja' :
			return [
				('interest', 'アニメ'), 		# 动漫同好
				('technology', '情報技術'), 
				('media', 'メディア'), 
				('sport', '体育'), 			# 体育运动
				('art', '芸術'), 			# 艺术表演 + 艺术设计
				('campus', '経営管理'), 
				('charity', '慈善'), 		# 慈善公益
				('nature-sci', '自然科学'), 
				('social-sci', '社会科学'), 
				('business', '商業'), 		# 商业经营
				('stage', 'ステージデザイン'), 
				('manufacture', '手芸'), 	# 手工制作
				('publishment', '文芸'), 	# 文学出版
				('language', '言語'), 		# 语言学习
				('other', 'その他'), 
			]
		return [
			('interest', '动漫'), 		# 动漫同好
			('technology', '信息技术'), 
			('media', '影视新闻传媒'), 
			('sport', '体育'), 			# 体育运动
			('art', '艺术'), 			# 艺术表演 + 艺术设计
			('campus', '校园管理'), 
			('charity', '慈善'), 		# 慈善公益
			('nature-sci', '自然科学'), 
			('social-sci', '社会科学'), 
			('business', '商业'), 		# 商业经营
			('stage', '舞台设计'), 
			('manufacture', '手工'), 	# 手工制作
			('publishment', '文学'), 	# 文学出版
			('language', '语言'), 		# 语言学习
			('other', '其他'), 
		]

	def category_exchange(category) :
		'英文->中文'
		return dict(ClubSnap.category_list()).get(category, '暂无')

	def contact_list(uid) :
		'返回cid组成的list，不包括关注'
		qry = AccountRelation.objects.filter(account_id_A=uid, 
			relation__in=('head', 'vice', 'core', 'member', 'member-wait'))
		return set(qry.values_list('account_id_B', flat=True))

	def club_find_by_uid(uid, attend=True, club=True) :
		'''
			通过uid获取用户参加的所有社团
			如果attend为True，返回用户参与的所有社团
				否则，返回用户关注的所有社团
			如果 club 为 True ，返回 ClubAccount 的 qry
				否则返回 cid list
		'''
		if attend :
			acc_set = AccountRelation.objects.filter(account_id_A=uid, 
				relation__in=('head', 'member', 'vice', 'core'))
		else :
			acc_set = AccountRelation.objects.filter(account_id_A=uid, 
				relation='follower')
		cid_set = set(acc_set.values_list('account_id_B', flat=True))
		if club :
			return ClubAccount.objects.filter(id__in=cid_set)
		else :
			return cid_set

	def club_find_by_cid(cid) :
		qry = ClubAccount.objects.filter(id=cid)
		if qry.count() != 0 :
			return qry[0]
		else :
			return None

	def intro_save(cid) :
		'从数据库查询intro并保存更新'
		mod = 2147483648
		club = ClubSnap.club_find_by_cid(cid)
		sintro_now = hash(club.simp_intro) % mod
		fintro_now = hash(club.full_intro) % mod
		qry = UpdateStatus.objects.filter(account_id=cid, relation='club')
		try :
			sintro_origin = qry.filter(category='simp_intro').order_by \
				('-time_update')[0].hash_value
		except IndexError :
			sintro_origin = -1
		try :
			fintro_origin = qry.filter(category='full_intro').order_by \
				('-time_update')[0].hash_value
		except IndexError :
			fintro_origin = -1
		if sintro_origin != sintro_now :
			UpdateStatus(account_id=cid, relation='club', 
				hash_value=sintro_now, content=club.simp_intro, 
				category='simp_intro').save()
		if fintro_origin != fintro_now :
			UpdateStatus(account_id=cid, relation='club', 
				hash_value=sintro_now, content=club.full_intro, 
				category='full_intro').save()

	def club_all_find() :
		'得到所有社团'
		return ClubAccount.objects.all()

	def club_all_info(export=False, args=None) :
		'''
			返回所有社团列表（用于导出）
			[危险] 这个功能可能导致数据泄漏，因此不应该在非 shell 环境使用
		'''
		qry = ClubSnap.club_all_find()
		club_list = []
		for i in qry :
			club_list.append({
				'data': i, 
				'head': ClubSnap.head_find_by_cid(i.id), 
			})
		if not export :
			return club_list
		else :
			ans = ''
			if args == None :
				args = ('id', 'sname', 'fname', 'head_name')
			for i in club_list :
				row = []
				if 'id' in args : row.append(str(i['data'].id))
				if 'sname' in args : row.append(str(i['data'].simp_name))
				if 'fname' in args : row.append(str(i['data'].full_name))
				if 'head_name' in args : row.append(str(i['head'].first_name))
				ans += '\t'.join(row) + '\n'
		return ans

	def alias_find_by_sname(alias) :
		'alias -> 实际名称'
		if ClubAccount.objects.filter(simp_name=alias).exists() :
			return alias
		try :
			cid = ClubAlias.objects.get(alias=alias, status=0).club_id
			return ClubAccount.objects.get(id=cid).simp_name
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def alias_all_by_cid(cid) :
		'cid -> 所有 alias 记录，返回 qry'
		return ClubAlias.objects.filter(club_id=cid, status=0).order_by('alias')

class AccountSnap:
	def url_safe(url) :
		'''
			判断 url 是否安全（例如 baidu.com 就非常不安全）
			期望的情况: '/club/hcc/?a=b&c=d'
			注意：不要带入引号，否则可能被注入
		'''
		if not url :
			return False
		try :
			path, search = url.split('?', 1)
		except ValueError :
			path = url
			search = None
		if not re.fullmatch('/([0-9a-zA-Z\_\-]+/)*', path) :
			return False
		if search == None :
			return True
		for i in search.split('&') :
			if not re.fullmatch('[0-9a-zA-Z\_\-]+=[0-9a-zA-Z\_\-]+', i) :
				return False
		return True

	def sname_find_by_aid(src, aid) :
		'得到社团或者用户的sname'
		return {
			'club': ClubSnap.sname_find_by_cid, 
			'user': UserSnap.sname_find_by_uid, 
		}.get(src, lambda x: None)(aid)

	def fname_find_by_aid(src, aid) :
		'得到社团或者用户的fname'
		return {
			'club': ClubSnap.fname_find_by_cid, 
			'user': UserSnap.fname_find_by_uid, 
		}.get(src, lambda x: None)(aid)

	def aid_find_by_sname(src, sname) :
		'返回account_id'
		try :
			return {
				'club': ClubSnap.cid_find_by_sname, 
				'user': UserSnap.uid_find_by_sname, 
				'forum': lambda x: ForumGroup.objects.get(status=0, 
														simp_name=x).id, 
			}.get(src, lambda x: None)(sname)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

	def sname_verify(request, src, sname) :
		'通过简称校验account_id有效性'
		return {
			'club': lambda r, s: ClubSnap.sname_verify(r, s), 
			'user': lambda r, s: UserSnap.sname_find_by_request(r) == s, 
		}.get(src, lambda r, s: False)(request, sname)

	def aid_verify(request, src, aid, vice=False, core=False) :
		'通过ID校验account_id有效性，认为vice>=core'
		return {
			'club': lambda r, a: ClubSnap.cid_verify(r, a, vice, core), 
			'user': lambda r, a: a and r.user.id == a, 
		}.get(src, lambda r, a: False)(request, aid)

	def contact_list(aid) :
		"[('club', cid), ('user', uid)]"
		return list(itertools.chain(
			zip(itertools.repeat('club'), ClubSnap.contact_list(aid)), 
			zip(itertools.repeat('user'), UserSnap.contact_list(aid)), 
		))

	def nickname_find_by_aid(src, aid) :
		'用户nickanme(sname)，社团sname'
		return {
			'user': UserSnap.nickname_find_by_uid, 
			'club': ClubSnap.sname_find_by_cid, 
		}.get(src, lambda x: '')(aid)

	def relation_check(ida, idb, relation) :
		'''
			Account 和 Account 的关系是否在 relation 中
			参见 AccountRelation 的定义
		'''
		assert type(relation) == tuple
		if AccountRelation.objects.filter(relation__in=relation, 
								account_id_A=ida, account_id_B=idb).exists() :
			return True
		# 如果是检查 uu-friend 等，需要反向确认
		if 'uu-friend' in relation :
			return AccountRelation.objects.filter(relation='uu-friend', 
								account_id_A=idb, account_id_B=ida).exists()
		return False

	def visit_count_by_account(account) :
		'自增并返回浏览数量，传入 club / user / share / event'
		account.visitors += 1
		account.save()
		return account.visitors

class QrcodeSnap :
	def qrcode_create(evid, src) :
		'生成qrcode，应该在生成时触发，返回True'
		fname_dict = {
			'event':	lambda evid: 'event-%d.png' % evid, 
			'share':	lambda evid: 'share-%s.png' % evid, 
			'club':		lambda evid: 'club-%s.png' % evid, 
			'user':		lambda evid: 'user-%s.png' % evid, 
		}
		val_dict = {
			'event':	lambda evid: '/event/%d/' % evid, 
			'share':	lambda evid: '/share/%s/' % evid, 
			'club':		lambda evid: '/club/%s/' % evid, 
			'user':		lambda evid: '/user/%s/' % evid, 
		}
		fname = fname_dict[src](evid)
		val = 'http://shierquan.tk' + val_dict[src](evid) + '?qrcode=true'
		media_route = 'images/qrcode/'
		try :
			qrcode.make(val).save(settings.MEDIA_ROOT + media_route + fname)
		except Exception:
			t,v,tb = sys.exc_info()
			print('v',val)
			print('r', settings.MEDIA_ROOT + media_route + fname)
			logger.error('t ' + str(t))
			logger.error('v ' + str(v))
		return True

	def qrcode_find(evid, src) :
		'生成qrcode地址，应该在创建活动时触发。'
		fname_dict = {
			'event':	lambda evid: 'event-%d.png' % evid, 
			'share':	lambda evid: 'share-%s.png' % evid, 
			'club':		lambda evid: 'club-%s.png' % evid, 
			'user':		lambda evid: 'user-%s.png' % evid, 
		}
		fname = fname_dict[src](evid)
		return '/media/images/qrcode/%s' % fname

	def qrcode_delete(evid, src) :
		'删除qrcode。返回True'
		fname_dict = {
			'event':	lambda evid: 'event-%d.png' % evid, 
			'share':	lambda evid: 'share-%s.png' % evid, 
			'club':		lambda evid: 'club-%s.png' % evid, 
			'user':		lambda evid: 'user-%s.png' % evid, 
		}
		fname = route_dict[src](evid)
		media_route = 'images/qrcode/'
		os.remove(settings.MEDIA_ROOT + media_route + fname)
		return True

	def qrcode_init() :
		'初始化share, event, club, user'
		#share
		from quan_share.models import ShareInfo
		qry = ShareInfo.objects.filter(status=0)
		for i in qry :
			QrcodeSnap.qrcode_create(i.attach_uuid, 'share')
		#event
		from quan_event.models import EventInfo
		qry = EventInfo.objects.filter(category__in=('history', ''))
		for i in qry :
			QrcodeSnap.qrcode_create(i.id, 'event')
		#club
		qry = ClubAccount.objects.all()
		for i in qry :
			QrcodeSnap.qrcode_create(i.simp_name, 'club')
		#user
		qry = UserAccount.objects.all()
		for i in qry :
			QrcodeSnap.qrcode_create(i.basic.last_name, 'user')

class CacheSnap :
	'''
		记录所有使用 cache 的地方，并提供消除
		
		缓存使用记录（一般会在 snap 的 documentation 中记录 "[缓]"）
			名称（用 jinja 语法表示）							受影响变量
			====================================================================
			loading_{{ ip }}_{{ progress_id }}				无（仅使用于文件上传）
			loaded_{{ ip }}_{{ progress_id }}				无（仅使用于文件上传）
			SquareSnap__total_rank__{{ cid }}				ava ev follow shr
			AvatarSnap__avatar_all__{{ src }}_{{ aid }}		avatar
			UserSnap__sname_find_by_uid__{{ uid }}			无
			UserSnap__fname_find_by_uid__{{ uid }}			无
			UserSnap__nickname_find_by_uid__{{ uid }}		Account.nickname
			ClubSnap__sname_find_by_cid__{{ cid }}			无
			ClubSnap__fname_find_by_cid__{{ cid }}			Club.full_name
			EventSnap__event_semester_find_by_cid__{{ src }}_{{ aid }}	event
			EventSnap__event_month_find_by_cid__{{ src }}_{{ aid }}		event
		
		当出现某些事件时，需要将缓存更新。以下函数直接删除相关数据，等待下一次访问时重新计算
	'''
	def avatar_uploaded(src, sname) :
		aid = AccountSnap.aid_find_by_sname(src, sname)
		if src == 'club' :
			cache.delete('SquareSnap__total_rank__%d' % aid)
		cache.delete('AvatarSnap__avatar_all__%s_%d' % (src, aid))

	def share_created(src, aid, attach_uuid) :
		if src == 'club' :
			cache.delete('SquareSnap__total_rank__%d' % aid)

	def event_created(src, aid, evid) :
		if src == 'club' :
			cache.delete('SquareSnap__total_rank__%d' % aid)

	def event_canceled(src, aid, evid) :
		if src == 'club' :
			cache.delete('EventSnap__event_month_find_by_cid__%s_%d'
															 % (src, aid))
			cache.delete('EventSnap__event_semester_find_by_cid__%s_%d'
															 % (src, aid))

	def club_follow(uid, cid, status) :
		'''
			status 说明: 
				0	取消
				1	跟随
		'''
		cache.delete('SquareSnap__total_rank__%d' % cid)

	def nickname_changed(uid) :
		cache.delete('UserSnap__nickname_find_by_uid__%d' % uid)

	def club_edited(cid) :
		cache.delete('ClubSnap__fname_find_by_cid__%d' % cid)

class AccountDicts :
	def club_edit(sname):
		club = ClubSnap.club_find_by_sname(sname)
		dict_edit = {'club': club, }
		dict_edit['category_list'] = ClubSnap.category_list()
		try :
			category = dict(dict_edit['category_list'])[club.category]
		except KeyError :
			category = dict(dict_edit['category_list'])['other']
		dict_edit['category'] = category
		return dict_edit

	def user_edit(request) :
		dict_render = {}
		user = UserSnap.account_find_by_request(request)
		dict_render['user'] = user
		dict_render['nickname'] = user.nickname
		dict_render['signature'] = user.signature
		return dict_render

class AccountViews :
	@never_cache
	def user_signup(request):
		'用户注册页面'
		dict_render = UserAgentSnap.record(request)
		
		next_url = request.GET.get('url') or request.POST.get('url', '')
		next_url = next_url.replace('&amp;', '&')
		if not AccountSnap.url_safe(next_url) :
			next_url = None

		if request.method == 'POST':
			recv_data = json.loads(request.POST.get('data', '{}'))
			bform = UserForm(recv_data)
			if not bform.is_valid():
				raise Snap.error('邮箱重复或表单输入有误')
			sname = bform.cleaned_data['last_name']
			rname = bform.cleaned_data['first_name']
			umail = bform.cleaned_data['username']
			error = UserSnap.sname_validate(sname)
			if UserSnap.email_validate(umail) == False :
				raise Snap.error('请重新输入邮箱地址')
			if UserAgentSnap.name_existed(rname) == False :
				raise Snap.error('该姓名不存在于学校数据库中')
			if UserAgentSnap.name_used(rname) :
				raise Snap.error('该姓名已被注册。')
			xform = UserAccountForm(recv_data)
			if not xform.is_valid():
				raise Snap.error('表单输入有误，请重新输入')
			phone = xform.cleaned_data['phone']
			grade = xform.cleaned_data['grade']
			if len(phone) != 11 or phone[0] != '1' :
				raise Snap.error('手机号码输入有误')
			if grade < 0 or grade > 6 :
				raise Snap.error('年级输入有误')
			if rname[0:2] != 't-' :
				status = 'student'
			else :
				status = 'teacher'

			buser = bform.save(commit=False)
			buser.set_password(bform.cleaned_data['password'])
			buser.save()
			xuser = xform.save(commit=False)
			xuser.basic = buser
			xuser.status = status
			xuser.pinyin = ''.join(pypinyin.lazy_pinyin \
				(xuser.basic.first_name))
			QrcodeSnap.qrcode_create(xuser.basic.last_name, 'user')
			xuser.save()
			assert(buser.id == xuser.basic_id)
			UserAgentSnap.name_update(rname, buser.id)
			request.session["welcome_flag"] = True
			PublicMessageAction.save \
				(request, 'user', 'new', xuser.basic.id, 'user')
			url = '/login/'
			if next_url :
				url = '/login/?url=%s' % parse.quote(next_url)
			return Snap.success(request, '成功注册。重定向至shierquan.tk/login/', 
								{ 'redirect': url })
		else :
			if next_url :
				dict_render['redirect_url'] = next_url
			sname = UserSnap.sname_find_by_request(request)
			if sname is not None :
				if next_url :
					return Snap.redirect(next_url)
				return Snap.redirect('/user/%s/' % sname)
			else :
				bform = UserAccountForm()
				dict_render['title'] = ' - 注册'
				return Snap.render('user_signup.html', dict_render)

	@never_cache
	@UserAuthority.logged_in
	def user_logout(request):
		dict_render = UserAgentSnap.record(request)
		host_id = request.session.get('host_id', '')
		auth.logout(request)
		request.session['host_id'] = host_id
		next_url   = request.GET.get('url')    or request.POST.get('url', '')
		next_url = next_url.replace('&amp;', '&')
		if AccountSnap.url_safe(next_url) :
			return Snap.redirect(next_url)
		else :
			return Snap.redirect('/')

	@never_cache
	def user_login(request):
		'用户登录页面'
		dict_render = UserAgentSnap.record(request)
		welcome_status = request.session.get('welcome_flag', False)
		request.session.set_test_cookie()

		next_src   = request.GET.get('module') or request.POST.get('module', '')
		next_id    = request.GET.get('id')     or request.POST.get('id', '')
		next_token = request.GET.get('token')  or request.POST.get('token', '')
		next_url   = request.GET.get('url')    or request.POST.get('url', '')
		next_url = next_url.replace('&amp;', '&')
		if not AccountSnap.url_safe(next_url) :
			next_url = None

		if request.method == 'POST':
			username = request.POST.get('username', '')
			password = request.POST.get('password', '')
			if UserAgentSnap.login_restrict(request, username) :
				raise Snap.error('您的请求被认为可能是攻击，请稍后重试')
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				auth.login(request, user)
				try :
					from quan_mobile.models import MobileHost
					host_id = request.session['host_id']
					MobileHost.objects.filter(host_id=host_id).update(
						account_id=UserSnap.uid_find_by_request(request))
				except Exception :
					pass
				if welcome_status == True and not next_url :
					request.session["welcome_flag"] = False
					sname = UserSnap.sname_find_by_request(request)
					return Snap.success(request, '登录成功，正在跳转', 
									{ 'redirect': '/avatar/user/%s/' % sname })
				else :
					if next_url :
						return Snap.success(request, '登录成功，正在跳转', 
											{ 'redirect': next_url })
					security = lambda x: re.fullmatch('[0-9a-zA-Z\_\-]+', x)
					if next_src in ('share', 'event', 'club', 'user', 'news') :
						if security(next_id) :
							url = '/%s/%s/' % (next_src, next_id)
							return Snap.success(request, '登录成功，正在跳转', 
												{ 'redirect': url })
					elif next_src == 'signup' :
						if security(next_id) and security(next_token) :
							url = '/event/signup/qrcode/?token=%s&evid=%s' % \
								(next_token, next_id)
							return Snap.success(request, '登录成功，正在跳转', 
												{ 'redirect': url })
					url = '/user/%s/' % UserSnap.sname_find_by_request(request)
					return Snap.success(request, '登录成功，正在跳转', 
										{ 'redirect': url })
			else:
				raise Snap.error('邮箱地址或密码错误')

		dict_render['next_id'] = next_id
		dict_render['next_token'] = next_token
		dict_render['next_src'] = next_src
		dict_render['title'] = ' - 登录'
		
		if next_url :
			dict_render['redirect_url'] = next_url
			dict_render['redirect_url_encode'] = parse.quote(next_url)

		if not request.session.test_cookie_worked() :
			dict_render['content'] = '请在浏览器上启用Cookies，否则您将无法登录。'
			return Snap.render('user_login.html', dict_render)
		if request.session.get('welcome_flag') == True :
			dict_render['welcome_flag'] = True
			return Snap.render('user_login.html', dict_render)
		sname = UserSnap.sname_find_by_request(request)
		if sname :
			if next_url :
				return Snap.redirect(next_url)
			else :
				return Snap.redirect('/user/%s/' % sname)
		else :
			return Snap.render('user_login.html', dict_render)

	def api_user_login(request) :
		'''
			允许通过调用 API 登录
			http://127.0.0.1:8000/api/login/?username=jkl@jkl.jkl&password=jkl
		'''
		dict_render = UserAgentSnap.record(request)
		username = request.GET.get('username', '')
		password = request.GET.get('password', '')
		if not UserAgentSnap.mobile_ua_test(request) :
			raise Snap.error('UA not found, please contact the admin')
		if UserAgentSnap.login_restrict(request, username) :
			raise Snap.error('Service Unavailable')
		user = auth.authenticate(username=username, password=password)
		if user is None or not user.is_active:
			raise Snap.error('Authentication error')
		auth.login(request, user)
		sessionid = request.session._get_session_key()
		exp_date = request.session.get_expiry_date()
		utn = datetime.utcnow()
		ltn = datetime.now()
		dt = timedelta(0, (ltn - utn).seconds, 0)
		ut = exp_date - dt
		print(exp_date)
		print(dt)
		from quan_avatar.views import AvatarSnap
		resp_data = {
			'sessionid': str(sessionid), 
			'expires': str(ut.strftime('%Y-%m-%dT%H:%M:%S.000Z')), 
			'path': '/', 
			'httpOnly': True, 
			'sname': user.last_name, 
			'fname': user.first_name, 
			'avatar': AvatarSnap.avatar_find('user', user.id, 'large'), 
		}
		return Snap.success(request, 'Login Success', resp_data)

	@vary_on_cookie
	@UserAuthority.logged_in
	def club_create(request):
		'注册社团'
		dict_render = UserAgentSnap.record(request)
		dict_render['category_list'] = ClubSnap.category_list()
		dict_render['title'] = ' - 创建社团'
		if request.method != 'POST':
			return Snap.render('club_create.html', dict_render)
		try :
			data = json.loads(request.POST.get('data'))
		except ValueError :
			raise Snap.error('数据错误')
		cform = ClubAccountForm(data)
		if not cform.is_valid():
			raise Snap.error('输入内容不完整或过长')
		sname = cform.cleaned_data['simp_name']
		error = ClubSnap.sname_validate(sname)
		nclub = cform.save()
		nclub.pinyin = ''.join(pypinyin.lazy_pinyin(nclub.full_name))
		nclub.save()
		uid = UserSnap.uid_find_by_request(request)
		ClubSnap.create(uid, nclub)
		QrcodeSnap.qrcode_create(nclub.simp_name, 'club')
		ClubSnap.intro_save(nclub.id)
		PublicMessageAction.save(request, 'club', 'new', uid, 
								'user', nclub.id, 'club')
		url = '/avatar/club/%s/' % nclub.simp_name
		return Snap.success(request, '社团创建成功', { 'redirect': url })

	@vary_on_cookie
	@UserAuthority.logged_in
	def club_follow(request, sname) :
		'[JSON] 用户跟随社团'
		dict_render = UserAgentSnap.record(request)
		from quan_message.views import MessageSnap
		if request.method != 'POST':
			raise Http404()
		resp_data = {}
		cid = ClubSnap.cid_find_by_sname(sname)
		fname = UserSnap.fname_find_by_request(request)
		uid = UserSnap.uid_find_by_request(request)
		if ClubSnap.follow(cid, request) :
			PublicMessageAction.save(request, 'club', 'follow', uid, 
									'user', cid, 'club')
			content = '成功订阅社团'
			CacheSnap.club_follow(uid, cid, 0)
		else :
			content = '成功退订社团'
			CacheSnap.club_follow(uid, cid, 1)
		return Snap.success(request, content, {
			'follower': ClubSnap.follower_total(cid), 
			'reload': True, 
		})

	@vary_on_cookie
	@UserAuthority.logged_in
	def club_join(request, sname) :
		from quan_message.views import MessageSnap
		'用户加入社团'
		dict_render = UserAgentSnap.record(request)
		cid = ClubSnap.cid_find_by_sname(sname)
		uid = UserSnap.uid_find_by_request(request)
		join_status = ClubSnap.join(cid, request)
		if join_status == False :
			PrivateMessageAction.save(
				'您已经成功退出%s' % ClubSnap.sname_find_by_cid(cid), 
					cid, 'club', uid, 'user', cid, 'club')
			return Snap.success(request, '成功退出社团，请刷新', 
								{ 'reload': True, 'status': 'primary' })
		elif join_status == True :
			PublicMessageAction.save(request, 'member', 'apply', uid, 'user', 
				cid, 'club')
			PrivateMessageAction.save(
				'欢迎加入%s' % ClubSnap.sname_find_by_cid(cid), 
					cid, 'club', uid, 'user', cid, 'club')
			return Snap.success(request, '成功提交申请，请等待审核', 
								{ 'reload': True, 'status': 'primary' })

	@vary_on_cookie
	@UserAuthority.logged_in
	def club_edit(request, sname):
		dict_render = UserAgentSnap.record(request)
		cid = ClubSnap.cid_find_by_sname(sname)
		UserAuthority.assert_permission(request, 'club', cid)
		if request.method == 'POST':
			try :
				data = json.loads(request.POST.get('data', ''))
			except json.decoder.JSONDecodeError :
				raise Snap.error('数据错误')
			qry = ClubSnap.club_find_by_cid(cid)
			if not qry :
				raise Http404()
			full_name = data.get('full_name', '')
			simp_intro = data.get('simp_intro', '')
			full_intro = data.get('full_intro', '')
			category = data.get('category', '')
			if category not in map(lambda x: x[0], ClubSnap.category_list()) :
				raise Snap.error('请选择分类')
			if not all((full_name, simp_intro, full_intro, category)) :
				raise Snap.error('表单填写不全')
			try :
				qry.full_name = full_name
				qry.simp_intro = simp_intro
				qry.full_intro = full_intro
				qry.category = category
				qry.save()
			except DataError :
				raise Snap.error('您输入的字数已经超出限制')
			ClubSnap.intro_save(cid)
			PublicMessageAction.save(request, 'club', 'update', 
									request.user.id, 'user', cid, 'club')
			CacheSnap.club_edited(cid)
			return Snap.success(request, '修改成功', 
								{ 'redirect': '/club/%s/' % sname })
		dict_render.update(AccountDicts.club_edit(sname))
		dict_render['title'] = t_(' - 编辑%s的信息') % \
									dict_render['club'].full_name
		return Snap.render('club_edit.html', dict_render)

	@vary_on_cookie
	@UserAuthority.logged_in
	def user_edit(request, sname):
		dict_render = UserAgentSnap.record(request)
		dict_render['title'] = ' - 编辑个人信息'
		uid = UserSnap.uid_find_by_request(request)
		if UserSnap.sname_find_by_request(request) != sname :
			raise Http403()
		if request.method == 'GET' :
			dict_render.update(AccountDicts.user_edit(request))
			return Snap.render('user_edit.html', dict_render)
		else :
			nickname = request.POST.get('nickname', '')
			signature = request.POST.get('signature', '')
			base = UserSnap.account_find_by_request(request)
			if nickname and base.nickname != nickname :
				base.nickname = nickname
				UpdateStatus(account_id=uid, relation='user', 
							content=nickname, category='nickname').save()
				CacheSnap.nickname_changed(uid)
			if signature and base.signature != signature :
				base.signature = signature
				UpdateStatus(account_id=uid, relation='user', 
							content=signature, category='signature').save()
			base.save()
			return Snap.success(request, '成功修改个人信息', 
								{ 'redirect': '/user/%s/' % sname })

	@vary_on_cookie
	def nickname(request) :
		dict_render = UserAgentSnap.record(request)
		uid = UserSnap.uid_find_by_request(request)
		if request.method == 'POST' :
			UserSnap.nickname_set(uid, nickname)
		return json.dumps({ 'nickname': UserSnap.nickname_find_by_uid(uid), })

	@vary_on_cookie
	@UserAuthority.logged_in
	def user_follow(request) :
		'break=break为取消，传送uid作为被跟随者的ID'
		dict_render = UserAgentSnap.record(request)
		host_id = request.POST.get('uid', '0')
		follower_id = UserSnap.uid_find_by_request(request)
		if not UserSnap.user_find_by_uid(host_id) :
			raise Snap.error('请指定被跟随者')
		if request.POST.get('break') == 'break' :
			UserSnap.follow_break(host_id, follower_id)
		else:
			UserSnap.follow(host_id, follower_id)
		PublicMessageAction.save(request, 'user', 'follow', follower_id, 'user', 
			host_id, 'user')
		return Snap.success(request, '操作成功', { 'reload': True })

	@vary_on_cookie
	@UserAuthority.logged_in
	def user_friend(request) :
		'[JSON] 操作好友关系； break=break 为删除/拒绝好友，传送 uid 作为被访问者的 ID'
		dict_render = UserAgentSnap.record(request)
		ida = UserSnap.uid_find_by_request(request)
		idb = request.POST.get('uid', '0')
		if not UserSnap.user_find_by_uid(idb) :
			raise Snap.error('请指定好友')
		friend_status = UserSnap.friend_status_find(idb, ida)
		if friend_status == 'friend' :
			if request.POST.get('break') == 'break' :
				UserSnap.friend_break(ida, idb)
			else :
				raise Snap.error('请通过传输break确认')
		elif friend_status == 'friend-waiting' :			# visitor 等待
			raise Snap.error('请耐心等待对方确认')
		elif friend_status == 'friend-waiting-reverse' :	# visitor 需要确认
			if request.POST.get('break') == 'break' :
				UserSnap.friend_deny(ida, idb)
			else :
				UserSnap.friend_check(ida, idb)
		else :	# none
			if not UserSnap.is_friend_annoy(ida, idb) :
				UserSnap.friend_wait(ida, idb)
				fname = UserSnap.fname_find_by_request(request)
				PrivateMessageAction.save('%s请求与您成为好友' % fname, 0, 
										'friend', idb, 'user', ida, 'user')
		return Snap.success(request, '操作成功', { 'reload': True })

	@vary_on_cookie
	def account_search(request, search_type) :
		"[JSON] 返回所有可能的结果，search_type in ('user', 'club', 'all')"
		dict_render = UserAgentSnap.record(request)
		query = request.POST.get('query') or request.GET.get('query')
		if not query :
			raise Snap.error('请输入查询内容')
		pool = []
		if search_type in ('user', 'all') :
			pool.append(UserSnap.user_search(query))
		if search_type in ('club', 'all') :
			pool.append(ClubSnap.club_search(query))
		ans = itertools.islice(itertools.chain.from_iterable(pool), 6)
		list_return = []
		from quan_avatar.views import AvatarSnap
		for i in ans :
			obj_dict = {}
			if type(i) == ClubAccount :
				obj_dict['type'] = 'club'
				obj_dict['s'] = '[社团]'
				obj_dict['h'] = i.full_name
				obj_dict['p'] = i.simp_intro
				obj_dict['a'] = '/club/%s/' % i.simp_name
				obj_dict['i'] = AvatarSnap.avatar_find('club', i.id, 'medium')
			else :
				obj_dict['type'] = 'user'
				u = UserSnap.account_find_by_uid(i.id)
				obj_dict['s'] = '[用户]'
				obj_dict['h'] = u.nickname
				obj_dict['p'] = u.signature
				obj_dict['a'] = '/user/%s/' % i.last_name
				obj_dict['i'] = AvatarSnap.avatar_find('user', i.id, 'medium')
			list_return.append(obj_dict)
		if not list_return :
			raise Snap.error('没能找到相关信息')
		else :
			return Snap.success(request, '', { 'obj': list_return })

	@vary_on_cookie
	def reset_password(request, sname) :
		dict_render = UserAgentSnap.record(request)
		dict_render['title'] = ' - 修改密码'
		if UserSnap.sname_find_by_request(request) != sname :
			raise Http403()
		if request.method == 'POST' :
			uid = UserSnap.uid_find_by_request(request)
			user = User.objects.filter(id=uid)[0]
			if not user.check_password \
				(request.POST.get('original_password', '')) :
				raise Snap.error('原密码错误')
			password = request.POST.get('password', '')
			if password == '' :
				raise Snap.error('密码不可为空')
			user.set_password(password)
			user.save()
			return Snap.success(request, '密码修改成功，请重新登录', 
								{ 'redirect': '/logout/' })
		else :
			return Snap.render('user_reset.html', dict_render)

	@vary_on_cookie
	def club_alias(request, sname) :
		dict_render = UserAgentSnap.record(request)
		if request.method != 'POST' :
			return Snap.redirect('/club/%s/' % sname)
		cid = ClubSnap.cid_find_by_sname(sname)
		UserAuthority.assert_permission(request, 'club', cid)
		action = request.POST.get('action', '')
		if action == 'add' :
			new_alias = request.POST.get('new_alias')
			if not new_alias or not re.match('[a-zA-Z\-]{1,30}$', new_alias) :
				raise Snap.error('填写30个以内的大小写字母或减号')
			if ClubAlias.objects.filter(club_id=cid, status=0).count() > 10 :
				raise Snap.error('链接太多了，请删除几个再试')
			if ClubSnap.alias_find_by_sname(new_alias) :
				raise Snap.error('这个名称已经被占用了')
			ClubAlias(alias=new_alias, club_id=cid).save()
			return Snap.success(request, '链接添加成功', { 'reload': True })
		elif action == 'delete' :
			alias = request.POST.get('alias')
			qry = ClubAlias.objects.filter(alias=alias, club_id=cid, status=0)
			if not qry :
				raise Snap.error('找不到记录，请刷新页面')
			qry.update(status=1)
			return Snap.success(request, '链接删除成功', { 'reload': True })
		else :
			raise Snap.error('参数错误')


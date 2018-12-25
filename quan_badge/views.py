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
from quan_auth.views import AuthSnap
from quan_avatar.views import AvatarSnap
from quan_message.views import PrivateMessageAction, PublicMessageAction
from quan_ua.views import *

class BadgeSnap:
	def badge_find_by_cid(src, aid) :
		'一个账户的所有徽章'
		return BadgeInfo.objects.filter \
			(relation=src, account_id=aid, status=0).order_by('-rank')

	def badge_total_by_cid(src, aid) :
		'一个账户的所有徽章数量'
		return BadgeInfo.objects.filter \
			(account_id=aid, relation=src, status=0).count()

	def remove(bid) :
		'删除徽章'
		BadgeInfo.objects.filter(id=bid).update(status=1)
		BadgeRelation.objects.filter(badge_id=bid).update(status=1)

	def withdraw(bid, uid) :
		'撤回向社团成员颁发的徽章'
		BadgeRelation.objects.filter(recv_id=uid, recv_relation='user', 
									badge_id=bid).update(status=1)

	def create_frequent(src, aid) :
		'是否提交频率过快'
		return BadgeInfo.objects.filter(relation=src, account_id=aid, status=0, 
			time_create__gte=datetime.now() - timedelta(0, 15)).exists()

	def grant(cid, fname, bid, reason) :
		'向社团成员授予徽章'
		uid = UserSnap.uid_find_by_fname(fname)
		if not uid :
			raise Snap.error('找不到接受者，请检查姓名拼写')
		if BadgeRelation.objects.filter(badge_id=bid, recv_id=uid, 
									recv_relation='user', status=0).exists() :
			raise Snap.error(t_('已经向%s授予过这枚徽章了') % fname)
		BadgeRelation(send_relation='club', send_id=cid, reason=reason, 
					recv_relation='user', recv_id=uid, badge_id=bid).save()

	def relation_find_by_bid(bid) :
		'获取获得某一徽章的全体成员'
		return BadgeRelation.objects.filter(badge_id=bid, status=0)

	def bid_verify(request, bid, vice=True) :
		'用户是否有权利使用徽章，如果是，返回 (aid, src) ，否则报错'
		try :
			qry = BadgeInfo.objects.get(id=bid, status=0)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			raise Http404('找不到徽章')
		src, aid = qry.relation, qry.account_id
		UserAuthority.assert_permission(request, src, aid)
		return src, aid

	def relation_find_by_uid(src, aid) :
		'用户获得的所有徽章'
		return BadgeRelation.objects.filter \
				(recv_id=aid, recv_relation=src, status=0)

	def badge_find_by_bid(bid) :
		try :
			return BadgeInfo.objects.get(id=bid, status=0)
		except (ObjectDoesNotExist, MultipleObjectsReturned) :
			return None

class BadgeDicts :
	def intro(src, aid):
		dict_intro = {
			'avatar': AvatarSnap.avatar_find(src, aid),
			'badge_list': BadgeSnap.badge_find_by_cid(src, aid),
			# badge_list => USer?
		}
		return dict_intro

	def badge_find(src, aid):
		'得到用户已获得的徽章列表'
		if aid == None :
			return None
		qry = BadgeSnap.relation_find_by_uid(src, aid)
		badge_list = []
		for i in qry :
			badge = BadgeSnap.badge_find_by_bid(i.badge_id)
			badge_list.append({
				'data': i, 
				'badge': badge,
				'club': ClubSnap.fname_find_by_cid(badge.account_id),
			})
		return badge_list

	def badge_user_find(bid):
		'得到所有获得特定徽章的用户列表'
		dict_render = {}
		qry = BadgeSnap.relation_find_by_bid(bid)
		name_list = []
		from quan_event.views import EventSnap
		for index, i in enumerate(qry) :
			grant_time, = ChineseSnap.datetime_simp(i.time_update),
			name_list.append({
				'uid': i.recv_id, 
				'counter': index, 
				'reason': i.reason, 
				'fname': AccountSnap.fname_find_by_aid(i.recv_relation, 
														i.recv_id), 
				'grant_time': grant_time[0] + grant_time[1], 
			})
		dict_render['name_list'] = name_list
		dict_render['name_len'] = len(name_list)
		dict_render['name_empty'] = not bool(name_list)
		return dict_render

class BadgeViews:
	@vary_on_cookie
	@UserAuthority.logged_in
	def badge_create(request):
		dict_render = UserAgentSnap.record(request)
		if request.method == 'POST':
			src = request.POST.get('src', '')
			aid = int(request.POST.get('aid', -1))
			UserAuthority.assert_permission(request, src, aid, True)
			if BadgeSnap.create_frequent(src, aid):
				raise Snap.error('提交频率过高')
			json_dict = json.loads(request.POST.get('data', ''))
			eform = BadgeInfoForm(json_dict)
			if not eform.is_valid():
				raise Snap.error('徽章内容不完整')
			else :
				einst = eform.save(commit=False)
				einst.account_id = aid
				einst.relation = src
				einst.save()
				fname = AccountSnap.fname_find_by_aid(src, aid)
				PublicMessageAction.save(request, 'badge', 'new', aid, 
					src, einst.id, 'badge')
				return Snap.success(request, '已成功创建徽章', 
									{ 'reload': True })
		else:
			raise Http404()

	@vary_on_cookie
	@UserAuthority.logged_in
	def badge_grant(request):
		'向社团成员授予徽章。'
		dict_render = UserAgentSnap.record(request)
		fname = request.POST.get('fname', '')
		bid = request.POST.get('bid', '0')
		reason = request.POST.get('reason', '')
		src, aid = BadgeSnap.bid_verify(request, bid)
		if not reason :
			raise Snap.error('不合规定的操作#badge')
		BadgeSnap.grant(aid, fname, bid, reason)
		uid = UserSnap.uid_find_by_fname(fname)
		PublicMessageAction.save \
			(request, 'badge', 'grant', uid, 'user', bid, 'badge')
		try :
			badge_name = BadgeSnap.badge_find_by_bid(bid).name
		except AttributeError :
			badge_name = ''
		PrivateMessageAction.save \
			('你获得了徽章 '+ badge_name, bid, 'badge', uid, 'user', aid, src)
		return Snap.success(request, '徽章授予成功', { 'reload': True })

	@vary_on_cookie
	def badge_list(request) :
		'[ajax] 公共社团主页显示徽章的授予人数'
		dict_render = UserAgentSnap.record(request)
		bid = int(request.POST.get('bid', '0'))
		qry = BadgeSnap.badge_find_by_bid(bid)
		if not qry :
			raise Snap.error('找不到徽章')
		return Snap.success(request, '', BadgeDicts.badge_user_find(bid))

	@vary_on_cookie
	def badge_remove(request):
		'删除徽章'
		dict_render = UserAgentSnap.record(request)
		bid = request.POST.get('bid', '0')
		BadgeSnap.bid_verify(request, bid)
		BadgeSnap.remove(bid)
		from quan_message.views import MessageSnap
		MessageSnap.message_delete('badge', bid)
		return Snap.success(request, '徽章删除成功', { 'reload': True })

	@vary_on_cookie
	def badge_withdraw(request) :
		'撤回给一个人的徽章'
		dict_render = UserAgentSnap.record(request)
		bid = request.POST.get('bid', '0')
		BadgeSnap.bid_verify(request, bid)
		try :
			uid = int(request.POST.get('uid'))
		except ValueError :
			raise Snap.error('参数错误')
		BadgeSnap.withdraw(bid, uid)
		# 由于看起来没有必要，没有撤回消息
		return Snap.success(request, '成功撤回了授予的徽章', { 'reload': True })


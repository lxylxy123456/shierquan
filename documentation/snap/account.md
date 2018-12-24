# Snap.md
* 包含 Snap 的类包括一些比较底层的函数
* 一般的查询方法在出现问题时都会返回 None
	* except (ObjectDoesNotExist, MultipleObjectsReturned)

## class UserSnap
* 提示：为了使文档简洁， Account = UserAccount

### 查询

#### 和用户本身相关
* UserSnap.account_find_by_request(request)	request			Account
* UserSnap.uid_find_by_request(request)		request			User.id
* UserSnap.sname_find_by_request(request)	request			User.last_name
* UserSnap.fname_find_by_request(request)	request			User.first_name
* UserSnap.sname_find_by_uid(uid)			User.id 		User.last_name	[缓]
* UserSnap.fname_find_by_uid(uid)			User.id 		User.first_name	[缓]
* UserSnap.grade_find_by_uid(uid, chinese)	User.id			Account.grade
* UserSnap.uid_find_by_sname(sname)			User.last_name	User.id
* UserSnap.uid_find_by_fname(fname)			User.first_name	User.id
* UserSnap.user_find_by_uid(uid)			User.id			User
* UserSnap.account_find_by_uid(uid)			User.id			Account
* UserSnap.nickname_find_by_uid(uid)		User.id			Account.nickname
* UserSnap.signature_find_by_uid(uid)		User.id			Account.signature
* UserSnap.user_search(query)				query			yield User
* UserSnap.person_info(fname)				User.first_name	详细信息（仅维护用）

#### 用户之间的关系
##### 返回 bool
* UserSnap.is_friend(ida, idb)					ida <=> idb 是否是好友
* UserSnap.friend_status_find(ida, idb)			ida <=> idb 的好友情况（返回字符串）
* UserSnap.is_friend_annoy(ida, idb)			ida  => idb 扰民（被拒 3 次以上）
* UserSnap.is_follower(host_id, follower_id)	follower  => host 是否关注
* UserSnap.is_contact(host_id, follower_id)		follower  => host 关注或互为好友
##### 返回列表
* UserSnap.contact_list(uid)					uid <=> [User.id] 好友
* UserSnap.following_find(uid)					uid  => [User.id] 关注

### 操作
* UserSnap.signature_modify(uid, sign)			修改 uid 的 签名
* UserSnap.nickname_set(uid, nickname)			修改 uid 的 昵称
* UserSnap.friend_wait(ida, idb)				ida  => idb 请求好友
* UserSnap.friend_check(ida, idb)				ida <=> idb 确认好友
* UserSnap.friend_break(ida, idb)				ida <=> idb 断开好友
* UserSnap.friend_deny(ida, idb)				ida <=> idb 拒绝好友
* UserSnap.follow(host_id, follower_id)			ida  => idb	关注
* UserSnap.follow_break(host_id, follower_id)	ida  => idb	取消关注

### 其他
* UserSnap.sname_validate(sname)				sname 是否可以被注册
* UserSnap.grade_translate(grade)				将 grade 翻译为 中文 [翻]
* UserSnap.email_validate(email)				是否是正常邮箱地址

## class ClubSnap
* 提示：为了使文档简洁， Club = ClubAccount
### 认证
* ClubSnap.sname_verify(request, sname, ...)	用户是否对 Club.simp_name 有权限
* ClubSnap.cid_verify(request, cid, vice, core)	用户是否对 Club.id 有权限

### 查询

#### 和社团本身相关
* ClubSnap.club_find_by_sname(sname)			Club.simp_name	Club
* ClubSnap.cid_find_by_sname(sname)		[会抛错]	Club.simp_name	Club.id
* ClubSnap.alias_find_by_sname(alias)			sname / alias	Club.simp_name
* ClubSnap.fname_find_by_cid(cid)		[缓]		Club.id			Club.full_name
* ClubSnap.sname_find_by_cid(cid)		[缓]		Club.id			Club.simp_name
* ClubSnap.head_find_by_cid(cid)				Club.id			head
* ClubSnap.head_id_find_by_cid(cid)				Club.id			head.id
* ClubSnap.head_sname_find_by_cid(cid)			Club.id			head.last_name
* ClubSnap.vice_find_by_cid(cid)				Club.id			vice
* ClubSnap.leader_find_by_cid(cid)				Club.id			[head, vice]
* ClubSnap.club_find_by_cid(cid)				Club.id			Club
* ClubSnap.alias_all_by_cid(cid)				Club.id			[ClubAlias]
* ClubSnap.club_search(query)					query			[Club]
* ClubSnap.club_all_find()						无				[Club] 所有
* ClubSnap.club_total()							无				社团总数
* ClubSnap.club_all_info(export, args)			无				所有社团（仅维护）

#### 用户和社团之间的关系
##### 返回 bool
* ClubSnap.club_followed_by_uid(uid, cid)			uid      => cid 跟随
* ClubSnap.club_joined_by_uid(uid, cid)				uid      => cid 加入或等待审核
* ClubSnap.club_union_check(request)				request  => union 核心以上
##### 返回字符串
* ClubSnap.club_position_by_uid(cid, uid)			uid      => cid 关系情况 [翻]
##### 返回计数
* ClubSnap.follower_total(cid)						[len]    => cid 关注
* ClubSnap.member_total(cid)						[len]    => cid 加入
##### 返回列表
* ClubSnap.follower_find(cid)						[qry]    => cid 关注
* ClubSnap.follower_list(cid, return_type)			[可选]    => cid 关注
* ClubSnap.member_all(cid)							[uid]    => cid 加入
* ClubSnap.member_wait_find(cid)					[qry]    => cid 等待审核
* ClubSnap.contact_list(uid)						uid      =>[cid]所属或等待审核
* ClubSnap.club_find_by_uid(uid, attend, club)		uid      =>[cid]所属 or 跟随
* ClubSnap.grade_list_by_cid(cid)					成员的 [Account.grade]
##### 其他
* ClubSnap.attendence_total(uid, cid)				uid      => cid 加入时间

### 操作
* ClubSnap.create(request, nclub)				用 request 创建社团
* ClubSnap.join(cid, request)					request 加入或退出 cid
* ClubSnap.follow(cid, request)					request 关注或取消关注 cid
* ClubSnap.head_change(cid, fname, force)		将 cid 的 社长 交接为 fname
* ClubSnap.vice_change(cid, fname)				将 cid 的 副社长 交接为 fname
* ClubSnap.wait_reject(cid, uid)				拒绝 uid 对 cid 的申请加入
* ClubSnap.wait_member(cid, uid)				同意 uid 对 cid 的申请加入
* ClubSnap.member_remove(cid, uid)				删除 uid 在 cid 的职位
* ClubSnap.member_core(cid, uid)				将 uid 在 cid 设置或解除核心
* ClubSnap.intro_save(cid)						记录社团的介绍（历史查询用）
#### 已禁用
* ClubSnap.club_remove(cid)						删除社团
* ClubSnap.intro_truncate()						将 simp_intro 缩短

### 其他
* ClubSnap.sname_validate(sname)				sname 是否可以被注册
* ClubSnap.category_list()						社团联盟列表
* ClubSnap.category_exchange(category)			翻译社团联盟 英文 => 中文 [翻]

## class AccountSnap
* 		表记			社团				用户
	* src		'club'			'user'
	* aid		Club.id (cid)	User.id (uid)
	* sname		Club.simp_name	User.last_name
	* fname		Club.full_name	User.first_name
	* nickname	Club.simp_name	Account.nickname	

### 认证
* AccountSnap.url_safe(url)								url 是否安全
* AccountSnap.sname_verify(request, src, sname)			通过 simp_name 判断
* AccountSnap.aid_verify(request, src, aid, vice, core)	通过 cid / uid 判断

### 查询
* AccountSnap.sname_find_by_aid(src, aid)		aid				simp_name
* AccountSnap.fname_find_by_aid(src, aid)		aid				full_name
* AccountSnap.aid_find_by_sname(src, sname)		simp_name		aid
* AccountSnap.nickname_find_by_aid(src, aid)	aid				nickname

#### 账户之间的关系
##### 返回 bool
* AccountSnap.relation_check(ida, idb, relation)	检查账户关系（比较底层）
##### 返回列表
* AccountSnap.contact_list(aid)						aid 的联系人列表

### 其他
* AccountSnap.visit_count_by_account(account)		自增并返回浏览数量

## class CacheSnap
* CacheSnap.avatar_uploaded(src, aid)				上传头像时触发
* CacheSnap.share_created(src, aid, attach_uuid)	创建分享时触发
* CacheSnap.event_created(src, aid, evid)			创建活动时触发
* CacheSnap.event_canceled(src, aid, evid)			取消活动时触发
* CacheSnap.club_follow(uid, cid, status)			用户跟随/取消社团时触发
* CacheSnap.nickname_changed(uid)					更改昵称时触发
* CacheSnap.club_edited(cid)						社团基本信息更改时触发


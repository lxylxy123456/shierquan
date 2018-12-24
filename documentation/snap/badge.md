## class BadgeSnap

### 认证
* BadgeSnap.bid_verify(request, bid, vice)		是否有徽章操作权限，返回 (id, src)
* BadgeSnap.create_frequent(src, aid)			是否频繁创建

### 查询
* BadgeSnap.badge_find_by_cid(src, aid)			Club.id		[Badge]		创建
* BadgeSnap.badge_total_by_cid(src, aid)		Club.id		len [Badge]	创建数量
* BadgeSnap.badge_find_by_bid(bid)				Badge.id	Badge
* BadgeSnap.relation_find_by_bid(bid)			Badge.id	[Relation]
* BadgeSnap.relation_find_by_uid(src, aid)		User.id		[Relation]	获得

### 操作
* BadgeSnap.remove(bid)							删除徽章及其关系
* BadgeSnap.withdraw(bid, uid)					撤回赠送的徽章
* BadgeSnap.grant(cid, fname, bid, reason)		赠送徽章


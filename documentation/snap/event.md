## class EventSnap

### 认证
* EventSnap.create_frequent(src, aid, history)		是否投递活动太频繁

### 查询
* EventSnap.event_find_by_evid(evid)				Event.id	Event
* EventSnap.event_find_by_cid(src, aid, history)	Club.id		[Event]	所属关系
* EventSnap.event_month_find_by_cid(src, aid)	[缓]	Club.id		[Event]	一个月内
* EventSnap.event_semester_find_by_cid(src, aid)[缓]	Club.id		[Event]	一学期内
* EventSnap.event_next_find_by_cid(src, aid)		Club.id		Event	未结束
* EventSnap.event_filter_by_request(request)		request		[Event]	所属社团
* EventSnap.quest_find_by_evid(evid)				Event.id	Quest
* EventSnap.signed_get_by_event(event)				Event		[dict_render]
* EventSnap.follower_find_by_evid(evid)				Event.id	[dict_render]
* EventSnap.event_search(query)						query		[Event]
* EventSnap.signup_qrcode_find_by_evid(evid)		Event.id	签到二维码链接

### 活动和用户的关系
#### 判断
* EventSnap.quest_set_by_evid(evid)					evid 是否设置了签到
* EventSnap.signed_find_by_uid(evid, uid)			uid 是否签到过
* EventSnap.niced_find_by_request(request, evid)	request 是否已经赞过 evid
* EventSnap.followed_find_by_request(request, evid)	request 是否已经跟随过 evid
* EventSnap.signup_qrcode_check(evid, token)		签到的 二维码token 是否正确
#### 统计
* EventSnap.follower_total(evid)					关注数量
* EventSnap.nice_total(evid)						赞数量
* EventSnap.signup_total(evid)						成功签到的数量
#### 参与统计
* EventSnap.event_find_by_uid(uid)					User.id		[Event]	签到成功
* EventSnap.event_attendence_by_uid(uid, cid, ...)	User.id		参与时间, 总时间

### 操作
* EventSnap.event_signup(evid, uid, answer, manual)	签到
* EventSnap.remove(request, src, aid, evid)			删除活动
* EventSnap.follower_create(evid, uid)				关注
* EventSnap.nice_create(evid, uid)					赞
* EventSnap.signup_qrcode_create(evid)				创建签到二维码

### 其他
* EventSnap.semester_start(now=None)				当前学期的开始
* EventSnap.time_convert(json_dict, name)			将时间字符串转换为 datetime
* EventSnap.time_status(event)						活动时间情况
* EventSnap.history_check(time_set, time_end)		是否应该作为历史活动处理


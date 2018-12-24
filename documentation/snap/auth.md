## class AuthSnap

### 统计和排名
* AuthSnap.qrank_calc(cid)					社团等级（用于 /auth/edit/ ）
* AuthSnap.mrank_calc(uid, cid)				社员等级（用于显示活动签到情况）
* AuthSnap.ratio_join(uid, cid)				社员参与率，按月（用于显示活动签到情况）
* AuthSnap.active_check(uid, cid)			社员是否活跃，按月
* AuthSnap.active_total(cid)				活跃成员总数，按月
* AuthSnap.active_ratio(cid)				活跃成员比例，按月
* AuthSnap.join_ratio(cid)					出勤率（算法有问题）

### 主页通知
* AuthSnap.notice_read(uid)					标记为已阅读通知
* AuthSnap.notice_check(uid, note)			是否已经阅读通知

### 坏行为记录（暂未投入使用）
* AuthSnap.amercement_add(cid, data)		添加坏行为记录
* AuthSnap.amercement_del(amid)				删除坏行为记录
* AuthSnap.amercement_num(cid)				统计坏行为记录

### 星级申请
* AuthSnap.star_calc(cid, ...)				可以申报的星级（用于星级申请）
* AuthSnap.apply_statistics()				每个星级的申报数量（仅维护）

#### 2017年初新功能：自动算分
* AuthSnap.category_list(uid)				用户可以管理联盟的代号列表
* AuthSnap.get_rubric(category='global')	得到联盟或整体的星级评分准则

### 资金申请
* AuthSnap.funds_document_generate(...)		根据信息生成资金申请表

### 其他
* AuthSnap.form_fetch(cid)					社团最后上传的申请表（分享类型为 form ）


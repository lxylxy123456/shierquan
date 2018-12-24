## class ForumSnap

### 认证
* ForumSnap.forum_admin_verify(request)				HCC正社长
* ForumSnap.forum_core_verify(request)				社联核心成员
* ForumSnap.group_admin_verify(request, gid)		是否是 Group 的管理员
* ForumSnap.admin_verify(src, aid, request)			是否有删除权限
* ForumSnap.edit_verify(src, request, qry)			是否有更改权限
* ForumSnap.creator_verify(src, request, ...)		是否有言论权限
* ForumSnap.view_verify(src, request, ...)			是否有查看权限
* ForumSnap.sname_validate(sname)					是否可以为 group 注册该简称
* ForumSnap.replied(src, aid)						是否被回复（不可以删除）

### 查询
* ForumSnap.group_all()							所有板块			Group
* ForumSnap.thread_find_by_gid(gid)				Group.id		[Thread]
* ForumSnap.group_find_by_gid(gid)				Group.id		Group
* ForumSnap.sname_find_by_gid(gid)				Group.id		Group.simp_name
* ForumSnap.fname_find_by_gid(gid)				Group.id		Group.full_name
* ForumSnap.group_find_by_sname(sname)			Group.simp_name	Group
* ForumSnap.gid_find_by_sname(sname)			Group.simp_name	Group.id
* ForumSnap.response_find_by_rid(rid)			Response.id		Response
* ForumSnap.response_find_by_thid(thid)			Thread.id		[Response]
* ForumSnap.thread_find_by_thid(thid, gid)		Thread.id		Thread
* ForumSnap.thid_find_by_rid(rid)				Response.id		Thread.id
* ForumSnap.gid_find_by_thid(thid)				Thread.id		Group.id
* ForumSnap.url_find_by_thread(thread)			Thread			url
* ForumSnap.attach_wrap(suid)					attach_uuid		dict_render
* ForumSnap.public_thread_list()								[Thread] 非私有
* ForumSnap.thread_latest_render()								[dict_render]

### 操作
* ForumSnap.delete(src, aid)					删除（没有判断权限）
* ForumSnap.recursive_delete(src, aid)			递归删除，已禁用


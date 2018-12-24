## class ShareSnap
* suid = share uuid = Share.attach_uuid

### 认证
* ShareSnap.limit_check(src, aid)					是否符合 一天最多10个
* ShareSnap.share_frequent(src, aid)				是否符合 间隔至少5秒

### 查询
* ShareSnap.uuid_find_by_sid(sid)					Share.id	suid
* ShareSnap.share_find_by_sid(sid)					Share.id	Share
* ShareSnap.share_find_by_uuid(suid)				suid		Share
* ShareSnap.share_find_by_aid(src, aid)				src  aid	[Share]
* ShareSnap.sid_find_by_uuid(suid)					suid		Share.id
* ShareSnap.download_find(suid, tid, archive='')	suid tid	下载文件所需信息
* ShareSnap.thumbnail_find(suid, size, tid='')		suid (tid)	图像/视频截图链接
* ShareSnap.url_find_by_attach(attach)				Attach		下载链接
* ShareSnap.union_record_find()						社联通知		dict_render
* ShareSnap.file_list_find_by_suid(suid, ...)		suid		[dict_render]
* ShareSnap.image_list_find_by_suid(suid)			suid		[dict_render]
* ShareSnap.stream_list_find_by_suid(suid)			suid		[dict_render]
* ShareSnap.attach_find_by_uuid(attach_uuid)		suid		[Attach]
* ShareSnap.image_list_by_aid(src, aid)				src  aid	[Attach] 是图片
* ShareSnap.share_search(query)						query		[Share]
* ShareSnap.presentation_find_by_aid(...)			src  aid	[dict_render]

### 文件处理
* ShareSnap.stream_process(qry, file_type)			处理视频 - 转换为 mp4 或 webm
* ShareSnap.add_process()							添加守护进程
* ShareSnap.stream_thumbnail(mod, sname=None)		处理视频 - 截图
* ShareSnap.muti_create(...)						保存上传的文件
* ShareSnap.size_calc(qry)							计算 share 的附件大小之和
* ShareSnap.share_thumbnail(sname, name)			创建缩略图
* ShareSnap.archive_create(suid)					创建压缩包

### mix: 根据社团分享的图片生成 3*3 大图
* ShareSnap.mix_find(sname)
* ShareSnap.mix_create(cid)
* ShareSnap.three_square(pictures)

### 分享讨论，已放弃维护。建议移动到新闻
* ShareSnap.chat_find(sid)
* ShareSnap.chat_save(sid, cont, uid)
* ShareSnap.chat_frequent(uid, suid)
* ShareSnap.chat_message_notify_find(sid)

### 其他
* ShareSnap.uuid_create()							创建一个 uuid


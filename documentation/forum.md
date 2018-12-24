## forum
* 关系
	* 板块组	Topic	# 通过 Group.topic 决定
	* 板块	Group
	* 帖子	Thread
	* 回复	Response

### 任务
* 前端：quan_forum/templates/
	* 0 group.html 搜索"{% if is_admin %}"，在 Buttons 添加管理者的控制按钮。
		* 其中一个按钮是跳转到avatar（已经写了），你需要将其美化并且更改管理者按钮的位置
	* 0	完成 thread.html
		* 我已经将可能使用到的变量放到页面上。如果你没有数据，可以向我要。
	* 0	通过forum.html中的{{ is_admin }}判断是否管理员，如果是，增加Group的删除按钮
		* /forum/{{ group_sname }}/delete/, POST
	* 0	添加删除thread/response的按钮，判断为{% if if_admin %}
		* 路径为thread的访问路径加上“/delete/”，POST
	* 0	添加group/thread/response的底部栏/模态窗
* 0	后端
	* 模式
		* 隐秘模式[仅发送者和HCC核心成员可见]：
			* 申请密码重置
			* Bug Report
		* 开放模式[所有人可见]
			* 社团间合作
			* 十一圈远景构想
	* HINT
		* 可以更改avatar
	* TODO
		* ForumResponse.reply_id / reply_relation 问题
		* 删除时维护 Thread.response_number
	* 需要维护字段
		* Thread.time_update		最后修改时间
		* Thread.response_number	回复数量（最开始是0）

### 架设环境的代码
* ForumGroup(account_id=1, relation='user', simp_name='a', subject='sa', content='ca', topic='jkl').save()
* ForumGroup(account_id=1, relation='user', simp_name='b', subject='sb', content='cb', topic='jkl').save()
* ForumGroup(account_id=1, relation='user', simp_name='c', subject='sc', content='cc', secret=True, topic='jkljkl').save()
* ForumThread(send_id=1, send_relation='user', subject='s1', content='c1', group_id=1).save()
* ForumThread(send_id=1, send_relation='user', subject='s2', content='c2', group_id=1).save()
* ForumThread(send_id=1, send_relation='user', subject='s3', content='c3', group_id=2).save()
* ForumResponse(send_id=1, send_relation='user', reply_id=1, reply_relation='user', content='cc1', thread_id=1).save()
* ForumResponse(send_id=1, send_relation='user', reply_id=1, reply_relation='user', content='cc2', thread_id=1).save()
* ForumResponse(send_id=1, send_relation='user', reply_id=1, reply_relation='user', content='cc3', thread_id=1).save()


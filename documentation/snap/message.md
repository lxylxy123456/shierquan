## class PublicMessageAction
* PublicMessageAction.prompt_create_en(...)		英文版
* PublicMessageAction.prompt_create(...)		生成主语和宾语之间的三段文字 [翻]
* PublicMessageAction.save(...)					添加公共消息		[和别的模块有关]
* PublicMessageAction.find(...)					查找公共消息
* PublicMessageAction.account_info_find(...)	(src, aid) -> dict_render
* PublicMessageAction.wrap(qry)					qry -> dict_render
* PublicMessageAction.relation_filter(...)		过滤不相关消息

## class PrivateMessageAction
* PrivateMessageAction.save(...)				添加私人消息 		[和别的模块有关]
* PrivateMessageAction.follower_send(...)		推送给社团的跟随者	[和别的模块有关]
* PrivateMessageAction.find(...)				寻找用户的某个群组
* PrivateMessageAction.all(...)					和用户相关的所有群组的信息
* PrivateMessageAction.get_host(qry, recv_id)	计算消息所属群组
* PrivateMessageAction.link_find(...)			查找链接
* PrivateMessageAction.chat_wrap(qry, recv_id)	包装消息

## class MessageSnap
* MessageSnap.update_situation(request)			计算前端的更新请求
* MessageSnap.message_delete(src, aid)			删除相关信息		[和别的模块有关]


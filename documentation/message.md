## Message 获取 API
* [JSON] [GET] /message/global/
	* 参数 status 说明:
		* -1	更新早于 -time_create	的 16 条消息，尽可能晚
		* 0		更新最新				的 16 条消息
		* 1		更新晚于 time_create	的 16 条消息，尽可能早
			* 为了防止攻击，最多允许 30 分钟
	* 返回值
		* JSON		{'msglist', 'time_update', }
		* GlobalMessage	'msglist' {
			'platform': '#平台',
			'head': '#头部文本',
			'body': '#主部文本',
			'tail': '#尾部文本',
			'time': {
				'ago':		'#时间差（例如：2分钟前）',
			}
			'major', 'minor': {
				'link': 	'#链接地址',
				'text':		'#对象文本',	
				'image': 	'#缩略图（对应的用户头像/社团头像）',
			}
			
			''		某人		为活动	hccev	点了赞
			head	major 	body	minor	tail
		}
* [JSON] /message/private/
	* 参数 status 说明:
		* -1	更新早于 -time_create 的最后4条消息
		* 0		更新最近 4 条
		* 1		更新晚于 time_create 的条目
			* 为了防止攻击，最多允许 30 分钟
	* 返回值
		* PrivateMessage 'msglist' {
			* context		聊天对象sname
			* relation		聊天对象关系	'club' or 'user'
			* content		信息
			* sender		信息发送者
			* time_create	创建时间
			* url			链接地址
		}


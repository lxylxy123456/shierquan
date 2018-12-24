## class Snap
* Snap.success(request, content, update={})		返回成功信息（绿条）
* Snap.error(request, content, update={})		返回错误信息（黄条）（使用抛403实现）
	* 例外: email 中某个地方没有直接返回文本，因为实现过于麻烦
	* 例外: avatar 中没有使用，因为没有使用 ajax
* Snap.render(template, dict_render)			返回模板渲染（render_to_response）
* Snap.file(request, path, name, content_type)	返回文件下载

## class ChineseSnap
* ChineseSnap.timedelta_simp(delta)				7300s -> 2小时前
* ChineseSnap.timedelta_comp(delta)				7300s -> 2小时1分钟
* ChineseSnap.byte_exchange(byte_size)			1048576 -> 1.0 MiB
* ChineseSnap.datetime_comp(time_set)	[翻]		-> ('9月1日 星期四 ', '08:00')
* ChineseSnap.datetime_simp(time_set)	[翻]		-> ('9月1日 ', '08:00')

## class UserAgentSnap

### 视图函数的进入和返回
* UserAgentSnap.record(request)					记录请求日志，返回原始的 dict_render
	* [应该在所有视图函数开始的地方调用]

### 安全
* UserAgentSnap.ua_check(request)				访问者是否疑似自动访问器
* UserAgentSnap.examine(request)				检测洪水攻击（已经废弃）
* UserAgentSnap.login_restrict(...)				判断登录尝试是否太频繁
* UserAgentSnap.mobile_ua_test(request)			判断来自的客户端类型
* UserAgentSnap.mobile_strict_test(request)		通过类似bilibili的验证方法判断客户端

### 真实姓名
* UserAgentSnap.name_used(name)					真实姓名是否没有被注册
* UserAgentSnap.name_update(name, uid)			注册真实姓名
* UserAgentSnap.name_existed(name)				真实姓名是否存在
* UserAgentSnap.name_init()						初始化真实姓名数据库的底层版本
* UserAgentSnap.initialize(fix=0)				初始化真实姓名数据库（每学年手动执行）

### 统计
* UserAgentSnap.visit_count_by_sname(...)		计算访问次数
* UserAgentSnap.platform_find(request)			猜测访问者的终端所属平台
* UserAgentSnap.account_month_calc(src, sname)	一个月内的访问统计（未应用）

### 其他
* UserAgentSnap.grade_adhere()					猜测年级（已禁用）


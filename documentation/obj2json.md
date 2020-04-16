* 通过 getFormJson 将表单数据转化为Json格式
	* 用法: 在ajax请求中将表单传入

* 通过 getCookie(name) 获取标签为name的Cookie

* csrfSafeMethod 用于判断该请求是否需要加入csrfToken 

* 通过 ajaxBanner 将 ajax 请求标准化
	* 通过 Snap 的方法来渲染
		* 例如 Snap.success(request, '错误原因', { 状态字典 })
		* 状态字典
			* 'fade': 'false'			# 不隐藏“条”（默认为三秒隐藏）
			* 'redirect': '/login/'		# 重定向到 /login/
			* 'reload': True			# 刷新网页
	* 前端用法
		* ajaxBanner('网址', { POST参数 }, 'prepend位置', 
		* 	function(msg){ 可选处理函数，在默认的函数之前触发 })
		* 传输参数为 请求地址 请求的POST参数 结果的插入地点（CSS过滤字符串）
		* 对于客户端，需要添加 Ajax: true 于请求头
		* 如果希望希望该方法能够像普通的ajaxLoad()的方法运行，可以
			- prepend位置不写
			- function(msg)中返回字符串"preventDefault"

* banner_render 可用于渲染一个banner的前端模板

* 通过 ajaxSlow 防止 beta.shierquan.ercli.dev 出现 503
	* ajaxSlow 和 ajaxGet 类似，区别是阻止了同时请求一个资源的情况
		* 发送第二次请求时如果第一次没有结束，则会直接 return
	* 同时，如果请求返回了错误，会随机等待几个间隔，然后重新发送请求
		* 随机等待的时间间隔由 threshold 决定，会随着失败次数增加逐渐变大


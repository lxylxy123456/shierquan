function getFormJson(frm) {
	var o = {};
	var a = $(frm).serializeArray();
	$.each(a, function () {
		if (o[this.name] !== undefined) {
			if (!o[this.name].push) {
				o[this.name] = [o[this.name]];
			}
			o[this.name].push(this.value || '');
		} else {
			o[this.name] = this.value || '';
		}
	});
	return JSON.stringify(o);
}

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function ajaxBanner(ajax_url, ajax_data, prepend_location, func) {
	$.ajax({
		url: ajax_url,
		type: "POST",
		data: ajax_data,
		dataType: "json",
		beforeSend: function(xhr, settings) {
			xhr.setRequestHeader("Ajax", "true");
			var csrftoken = getCookie("csrftoken");
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		},
	}).done(function(msg){
		if (func != undefined) {
			if (func(msg) == "preventDefault") {
				prepend_location = "";
			}
		}
		if (!prepend_location) {
			return;
		}
		id = 'banner-message-' + Date.now();
		content = banner_render(msg.status, id, msg.content, msg.no_prefix);
		$(prepend_location).prepend(content);
		if (msg["fade"] != "false") {
			$("#" + id).fadeOut(3000);
		}
		if (msg["redirect"]) {
			setTimeout('window.location = "' + msg["redirect"] + '"', 1000);
		}
		if (msg["reload"]) {
			setTimeout('window.location.reload()', 1000);
		}
	}).fail(function(jqXHR, textStatus){
		if (ajax_url != "/message/private/") {
			alert("似乎与服务器通讯不畅...");
		}
	});
}

function banner_render(msg_type, id, content, no_prefix) {
	a = '<div class="alert alert-'; 						// msg_type
	b = ' alert-dismissible fade in" role="alert" id="';	// id
	c = '"><button type="button" class="close" data-dismiss="alert">'
	c += '<span aria-hidden="true">&times;</span><span class="'
	c += 'sr-only">Close</span></button><strong>';			// zh_type
	d = '</strong> ';										// content
	e = '</div>';
	if (no_prefix) {
		zh_type = '';
	}
	else {
		switch (msg_type) {
			case 'error': 
			case 'warning': 
				zh_type = '警告'; msg_type = 'warning'; break; 
			case 'success': 
				zh_type = '恭喜'; msg_type = 'success'; break; 
			case 'info': 
			case 'primary': 
				zh_type = '提示'; msg_type = 'info'; break; 
			default: zh_type = '';
		}
	}
	return a + msg_type + b + id + c + zh_type + d + content + e;
}

function ajaxGet(ajax_url, ajax_data, ajax_data_type, callback){
	ajax_data["Ajax"] = "true";
	$.ajax({
		url: ajax_url,
		type: "GET",
		data: ajax_data,	//名:值
		dataType: ajax_data_type,
	}).done(function(msg){
	//	data = JSON.parse(msg)
		callback(msg);
	});
}

var ajaxSlow_log = false;
function ajaxSlow(ajax_url, ajax_data, ajax_data_type, callback, interval) {
	// 一般用于 message 等不需要精准处理的地方
	var rec_life = 0;		// 0: 正常; 1: 正请求; 2: 出错
	var error_count = 0;
	var threshold = 2;
	function rec(){
		if (rec_life == 1) {
			if (ajaxSlow_log) {
				console.log("跳过等待");
			}
			return;
		}
		if (rec_life == 2) {
			error_count += Math.random();
			if (error_count > threshold) {
				error_count = 0;
				threshold += 0.5;
			}
			else {
				if (ajaxSlow_log) {
					console.log("跳过: " + error_count);
				}
				return;
			}
		}
		rec_life = 1;
		data = ajax_data()	// 注意：由于 data 可能改变，要传入 data 的生成函数
		data["Ajax"] = "true"
		$.ajax({
			url: ajax_url,
			type: "GET",
			data: data,
			dataType: ajax_data_type,
			beforeSend: function(xhr, settings) {
				var csrftoken = getCookie('csrftoken');
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			},
		}).done(function(msg){
			callback(msg);
			rec_life = 0;
		}).fail(function(jqXHR, textStatus){
			if (ajaxSlow_log) {
				console.log("似乎与服务器通讯不畅...");
			}
			rec_life = 2;
		});
	}
	rec();
	setInterval(rec, interval);
}


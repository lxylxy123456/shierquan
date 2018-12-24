'''

Copied from /usr/lib/python3.5/site-packages/django/views/defaults.py

Refer to 
https://docs.djangoproject.com/en/dev/topics/http/views/#customizing-error-views

提示：测试时需要关闭 DEBUG

'''

from django import http
from django.template import Context, Engine, TemplateDoesNotExist, loader
from django.utils import six
from django.utils.encoding import force_text
from django.views.decorators.csrf import requires_csrf_token

from translate import translate as t_

from django.conf import settings
import json, threading, logging

@requires_csrf_token
def page_not_found(request, exception, template_name='404.html'):
	exception_repr = ''
	try:
		message = exception.args[0]
	except (AttributeError, IndexError):
		pass
	else:
		if isinstance(message, six.text_type):
			exception_repr = t_(message, request)
	settings.request_thread_safe = threading.local()
	settings.request_thread_safe.request = request
	try :
		request.ua.status_code = 404
		request.ua.save()
	except Exception :
		pass
	if request.META.get('HTTP_AJAX') == 'true' :
		content_dict = {
			'status': 'error', 
			'content': exception_repr or t_('找不到页面', request), 
		}
		return http.HttpResponse(json.dumps(content_dict), 
								content_type="application/json")
	context = {
		'request_path': request.path,
		'exception': exception_repr,
		'request': request, 
	}
	try:
		template = loader.get_template(template_name)
		body = template.render(context, request)
		content_type = None
	except TemplateDoesNotExist:
		template = Engine().from_string('<h1>Not Found</h1><p>The requested URL'
						' {{ request_path }} was not found on this server.</p>')
		body = template.render(Context(context))
		content_type = 'text/html'
	return http.HttpResponseNotFound(body, content_type=content_type)


@requires_csrf_token
def server_error(request, template_name='500.html'):
	try:
		template = loader.get_template(template_name)
	except TemplateDoesNotExist:
		return http.HttpResponseServerError('<h1>Server Error (500)</h1>', 
											content_type='text/html')
	return http.HttpResponseServerError(template.render({ 'request': request }))


@requires_csrf_token
def bad_request(request, exception, template_name='400.html'):
	settings.request_thread_safe = threading.local()
	settings.request_thread_safe.request = request
	try :
		request.ua.status_code = 400
		request.ua.save()
	except Exception :
		pass
	try:
		template = loader.get_template(template_name)
	except TemplateDoesNotExist:
		return http.HttpResponseBadRequest('<h1>Bad Request (400)</h1>', 
											content_type='text/html')
	return http.HttpResponseBadRequest(template.render({ 'request': request }))

@requires_csrf_token
def permission_denied(request, exception, template_name='403.html'):
	settings.request_thread_safe = threading.local()
	settings.request_thread_safe.request = request
	try :
		request.ua.status_code = 403
		request.ua.save()
	except Exception :
		pass
	try:
		template = loader.get_template(template_name)
	except TemplateDoesNotExist:
		return http.HttpResponseForbidden('<h1>403 Forbidden</h1>', 
											content_type='text/html')

	content = t_(force_text(exception), request)
	if request.META.get('HTTP_AJAX') == 'true' :
		content_dict = {
			'status': 'error', 
			'content': content or t_('或许忘记登录？', request), 
		}
		return http.HttpResponse(json.dumps(content_dict), 
								content_type="application/json")
	return http.HttpResponseForbidden(
		template.render(request=request, context={
			'exception': content, 
			'content': content, 
			'request': request, 
			'prompt': '错误', 
		})
	)

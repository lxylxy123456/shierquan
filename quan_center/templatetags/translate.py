'''
	模板的翻译支持
	参考文档: https://docs.djangoproject.com/en/1.10/howto/custom-template-tags/
'''

from django import template
from translate import translate
from django.template.base import TOKEN_TEXT, TOKEN_VAR, render_value_in_context
from django.template import Node

register = template.Library()

@register.simple_tag
def t_(content) :
	return translate(content)

@register.simple_tag
def r_(content) :
	return content

# 以下代码已经废弃
'''
class BlockTranslateNode(Node) :
	def __init__(self, singular):
		self.singular = singular

	def render_token_list(self, tokens):
		result = []
		vars = []
		for token in tokens:
			if token.token_type == TOKEN_TEXT:
				result.append(token.contents.replace('%', '%%'))
			elif token.token_type == TOKEN_VAR:
				result.append('%%(%s)s' % token.contents)
				vars.append(token.contents)
		msg = ''.join(result)
		return msg, vars

	def render(self, context, nested=False):
		default_value = context.template.engine.string_if_invalid

		def render_value(key):
			if key in context:
				val = context[key]
			else:
				val = default_value % key if '%s' in default_value else default_value
			print('val', val)
			return render_value_in_context(val, context)

		for token in self.singular :
			if token.token_type == TOKEN_TEXT :
				print('txt', token.contents)
			else :
				print('tag', token.contents)
				print('tag ', render_value(token.contents))
				print('tag  ', render_value_in_context(token.contents, context))
				print('==', context['club_dict'])
	
		message_context = None
		tmp_context = {}
		context.update(tmp_context)
		singular, vars = self.render_token_list(self.singular)
#		result = translation.ugettext(singular)
		result = singular
		print(singular)
		


		data = {v: render_value(v) for v in vars}
		context.pop()
		try:
			result = result % data
		except (KeyError, ValueError):
			if nested:
				# Either string is malformed, or it's a bug
				raise TemplateSyntaxError(
					"'blocktrans' is unable to format string returned by gettext: %r using %r"
					% (result, data)
				)
			with translation.override(None):
				result = self.render(context, nested=True)
		return result


@register.tag
def tb_(parser, token) :
	cache = []
	while parser.tokens:
		token = parser.next_token()
		if token.token_type in (TOKEN_VAR, TOKEN_TEXT) :
			cache.append(token)
			print(token.contents.strip())
		else :
			break
	assert token.contents.strip() == 'endtb_'
	return BlockTranslateNode(cache)
'''

import re, os, sys, itertools

def tostr(obj) :
	if type(obj) == str :
		return obj
	else :
		return obj.tostr()

def join(items) :
	'猜测内容物之间是否有空格'
	items = list(items)
	if not items :
		return ''
	ans = items[0]
	for index, i in itertools.islice(enumerate(items), 1, None) :
		last = items[index - 1]
		space = 0	# 0: 中立; 1: 必须有; -1: 必须没有; 
		if re.fullmatch('\w+', last) and re.fullmatch('\w+', i) :
			space = 1
		if last in ('from', 'import') :
			space = 1
		if last in ('r', 'b', 'u') and i[0] in '\'\"' :
			space = -1
		# 处理
		ans += {0: '', 1: ' ', -1: ''}[space] + i
	return ans

class if_tag :
	def __init__(self, expression, code) :
		self.expression = expression
		self.code = code
	def __repr__(self) :
		return '<if %s: %s>' % (repr(self.expression), repr(self.code))
	def tostr(self, indent='') :
		return '%sif %s :' % (indent, self.expression.tostr()) + \
				self.code.tostr(indent + '\t', '\n')

class else_tag :
	def __init__(self, dropped, code) :
		self.code = code
	def __repr__(self) :
		return '<else: %s>' % repr(self.code)
	def tostr(self, indent='') :
		return '%selse :' % indent + self.code.tostr(indent + '\t', '\n')

class elif_tag :
	def __init__(self, expression, code) :
		self.expression = expression
		self.code = code
	def __repr__(self) :
		return '<elif %s: %s>' % (repr(self.expression), repr(self.code))
	def tostr(self, indent='') :
		return '%selif %s :' % (indent, self.expression.tostr()) + \
				self.code.tostr(indent + '\t', '\n')

class for_tag :
	def __init__(self, names, expression, code) :
		self.names = get_list(names)
		self.expression = expression
		self.code = code
	def __repr__(self) :
		return '<for %s in %s: %s>' % (repr(self.names), repr(self.expression), 
										repr(self.code))
	def tostr(self, indent='') :
		return '%sfor %s in %s :' % (indent, self.names.tostr(), 
										self.expression.tostr()) + \
				self.code.tostr(indent + '\t', '\n')

class with_tag :
	def __init__(self, names, expression, code) :
		self.names = get_list(names)
		self.expression = expression
		self.code = code
	def __repr__(self) :
		return '<with %s as %s: %s>' % (repr(self.names), repr(self.expression),
										repr(self.code))
	def tostr(self, indent='') :
		return '%swith %s as %s :' % (indent, self.names.tostr(), 
										self.expression.tostr()) + \
				self.code.tostr(indent + '\t', '\n')

class def_tag :
	def __init__(self, name, code) :
		self.name = name.word_list[0]
		assert len(name.word_list) == 2 and \
				type(name.word_list[1]) == bracket_tag
		self.arguments = get_list(name.word_list[1].content)
		self.code = code
	def __repr__(self) :
		return '<def %s(%s): %s>' % (repr(self.name), repr(self.arguments), 
									repr(self.code))
	def tostr(self, indent='') :
		return '%sdef %s(%s) :' % (indent, self.name, 
										self.arguments.tostr()) + \
				self.code.tostr(indent + '\t', '\n')

class class_tag :
	def __init__(self, name, code) :
		self.name = name.word_list[0]
		if len(name.word_list) > 1 :
			assert len(name.word_list) == 2 and \
					type(name.word_list[1]) == bracket_tag
			self.inherit = get_list(name.word_list[1].content)
		else :
			self.inherit = None
		self.code = code
	def __repr__(self) :
		if self.inherit :
			return '<class %s(%s): %s>' % (repr(self.name), repr(self.inherit), 
										repr(self.code))
		else :
			return '<class %s: %s>' % (repr(self.name), repr(self.code))
	def tostr(self, indent='') :
		if self.inherit :
			return '%sclass %s(%s) :' % (indent, self.name, 
											self.inherit.tostr()) + \
					self.code.tostr(indent + '\t', '\n')
		else :
			return '%sclass %s :' % (indent, self.name) + \
					self.code.tostr(indent + '\t', '\n')

class bracket_tag :
	def __init__(self, symbol) :
		self.symbol = symbol
		self.content = []
	def __repr__(self) :
		a = '\033[41m%s\033[0m'
		return a % self.symbol[0] + repr(self.content) + a % self.symbol[1]
	def __eq__(self, value) :
		return type(value) == bracket_tag and self.symbol == value.symbol and \
				self.content == value.content
	def tostr(self) :
		return join(map(tostr, self.content)).join(self.symbol)
	def append(self, obj) :
		self.content.append(obj)

class try_tag :
	def __init__(self, dropped, code) :
		self.code = code
	def __repr__(self) :
		return '<try: %s>' % repr(self.code)
	def tostr(self, indent='') :
		return '%stry :' % indent + self.code.tostr(indent + '\t', '\n')

class except_tag :
	def __init__(self, expression, code) :
		self.expression = expression
		self.code = code
	def __repr__(self) :
		return '<except %s: %s>' % (repr(self.expression), repr(self.code))
	def tostr(self, indent='') :
		return '%sexcept %s :' % (indent, self.expression.tostr()) + \
				self.code.tostr(indent + '\t', '\n')

class while_tag :
	def __init__(self, expression, code) :
		self.expression = expression
		self.code = code
	def __repr__(self) :
		return '<while %s: %s>' % (repr(self.expression), repr(self.code))
	def tostr(self, indent='') :
		return '%swhile %s :' % (indent, self.expression.tostr()) + \
				self.code.tostr(indent + '\t', '\n')

class name_list_tag :
	'可以用于def的参数列表或者for的枚举变量列表'
	def __init__(self, name_list) :
		if type(name_list) != list :
			name_list = name_list.word_list
		self.name_list = [name_list]
		while ',' in self.name_list[-1] :
			index = self.name_list[-1].index(',')
			self.name_list.append(self.name_list[-1][index + 1:])
			self.name_list[-2] = self.name_list[-2][:index]
	def __repr__(self) :
		return repr(self.name_list)
	def tostr(self) :
		return ', '.join(map(lambda x: join(map(tostr, x)), self.name_list))

class code_list_tag :
	'很多代码，在同一indent中（例如if里的内容）'
	def __init__(self) :
		self.code_list = []
	def yield_code(self, code) :
		self.code_list.append(code)
	def __repr__(self) :
		return repr(self.code_list)
	def tostr(self, indent=None, prefix='') :
		ans = prefix
		if prefix == '\n' and \
			all(map(lambda x: type(x) == code_tag, self.code_list)) :
			return ';'.join(filter(bool, map(lambda x: x.tostr(None, True), 
											self.code_list))) + '\n'
			# 以上压缩到一行
		for i in self.code_list :
			ans += i.tostr(indent or '')
		if not ans :	# 内容被忽略导致没有内容，需要填充 pass
			ans += (indent or '') + 'pass\n'
		return ans

class code_tag :
	'一段代码，理论上不包含分号'
	def __init__(self, word_list) :
		self.word_list = word_list
	def __repr__(self) :
		return repr(self.word_list)
	def tostr(self, indent=None, compressed=False) :
		if indent != None or compressed == True :
			if len(self.word_list) == 1 and type(self.word_list[0]) == str \
				and self.word_list[0][0] in '\'\"' :
				return ''	# doc string, 丢弃
		if indent == None :
			return join(map(tostr, self.word_list))
		else :
			return indent + join(map(tostr, self.word_list)) + '\n'

def get_indent(lines) :
	for i in lines :
		if not re.match('\s*(\#|$)', i) :
			return re.match('(\s*)\S', i).groups()[0]

def get_list(item_list) :
	assert item_list != None
	return name_list_tag(item_list)

def get_code(word_list) :
	return code_tag(word_list)

def read_expression(lines, end=';') :
	"end 为 ';' 时也会以行结尾"
	stack = []
	answers = code_list_tag()
	ans = []
	ans_generated = False
	while 1 :
		if not lines or not lines[0] :
			if lines :
				lines.pop(0)
			if end == ';' and not stack :	# 原: ans_generated
				if ans :
					answers.yield_code(get_code(ans))
				ans = []
				break
			continue
		if re.match('\s', lines[0][0]) :
			lines[0] = lines[0][1:]
			continue
		if lines[0].startswith(end) and not stack :
			if not (re.fullmatch('\w+', end) and 	# 防止出现 index -> in 的情况
					re.match('(\w+)', lines[0]).groups()[0] != end) :
				lines[0] = lines[0][len(end): ]
				if ans :
					answers.yield_code(get_code(ans))
				ans = []
				if end != ';' :
					break
				continue
		ans_generated = True
		re_symbol = '[\+\-\*\/\=\,\.\%\>\<\:\!\@\|\&\^]'
		if re.match('\w', lines[0]) :
			word, lines[0] = re.fullmatch('(\w+)(.*)', lines[0]).groups()
			([ans] + stack)[-1].append(word)
		elif lines[0][0] == '#' :
			lines.pop(0)
			if end == ';' and not stack :
				if ans :
					answers.yield_code(get_code(ans))
				ans = []
				break
		elif lines[0][0] == '\\' :
			assert len(lines[0]) == 1
			lines.pop(0)
		elif re.match(re_symbol, lines[0]) :
			word, lines[0] = re.fullmatch('(%s+)(.*)' % re_symbol,
											lines[0]).groups()
			([ans] + stack)[-1].append(word)
		elif re.match('[\(\[\{]', lines[0]) :
			pair = {'[': '[]', '{': '{}', '(': '()'}[lines[0][0]]
			stack.append(bracket_tag(pair))
			lines[0] = lines[0][1:]
		elif re.match('[\)\]\}]', lines[0]) :
			popped = stack.pop()
			assert popped.symbol[1] == lines[0][0]
			([ans] + stack)[-1].append(popped)
			lines[0] = lines[0][1:]
		elif lines[0][0] in '\'\"' :
#			print(lines[0], lines[1])
			for i in ("'''", '"""', '"', "'") :
				if lines[0].startswith(i) :
					break
			cache = i
			lines[0] = lines[0][len(i):]
			while lines :
#				print(lines[0])
				if not lines[0] :
					lines.pop(0)
					cache += '\n'
					continue
				if lines[0].startswith(i) :
					cache += i
					lines[0] = lines[0][len(i):]
					break
				elif lines[0][0] == '\\' :
					cache += lines[0][:2]
					lines[0] = lines[0][2:]
				else :
					cache += lines[0][0]
					lines[0] = lines[0][1:]
			([ans] + stack)[-1].append(cache)
		else :
			raise ValueError('Unknown character in: ' + repr(lines[0]))
	return answers

def read_code(lines, indent='') :
#	print('in', repr(indent), lines)
	ans = code_list_tag()
	while lines :
#		print(indent, lines)
		a = lines[0]
		if re.fullmatch('\s*', a) :
			lines.pop(0)
			continue
		i, c = re.fullmatch('(\s*)(\S.*)', a).groups()
#		print(lines)
		if i != indent and c[0] != '#' :
#			print(indent, repr((i, indent, c)))
			if indent.startswith(i) :	# 退出
				break
			raise IndentationError((i, c))	# 如果出现这个问题，可能因内部函数调用出错
#		print(repr(c))
#		key_word, remain = re.match('(\S+)((\s|$).*)', c).groups()[:2]
		key_word, remain = re.match('(\w*)((\W|$).*)', c).groups()[:2]
#		print('k', repr(key_word), repr(remain))
		key_dict = {
			'if': (if_tag, ':', ), 
			'for': (for_tag, 'in', ':', ), 
			'with': (with_tag, 'as', ':', ), 
			'def': (def_tag, ':', ), 
			'class': (class_tag, ':', ), 
			'else': (else_tag, ':', ), 
			'elif': (elif_tag, ':', ), 
			'try': (try_tag, ':', ), 
			'except': (except_tag, ':', ), 
			'while': (while_tag, ':', ), 
		}
		if key_word in key_dict :
#			print('kk', key_word)
			lines[0] = remain
			exp_list = []
			for i in key_dict[key_word][1:] :
#				print(lines[0])
				try :
					exp_list.append(read_expression(lines, i).code_list[0])
				except IndexError :
					exp_list.append(None)
			if not re.fullmatch('\s*(#.+)?', lines[0]) :	# inline
				exp_list.append(read_expression(lines, ';'))
			else :
				indent_son = get_indent(lines)
#				print('out', repr(indent), repr(indent_son), lines[:3])
				assert indent_son != indent and indent_son.startswith(indent)
				exp_list.append(read_code(lines, indent_son))
			ans.yield_code(key_dict[key_word][0](*exp_list))
		else :
			for i in read_expression(lines, ';').code_list :
				ans.yield_code(i)
	return ans

if __name__ == '__main__' :
	if not sys.argv[1:] :
		path = '/tmp/shiyiquan-fake/'
		if input('是否将 %s 覆盖？（回答イエス的英文）' % path) == 'yes' :
			for i in filter(lambda x: x.startswith('quan_'), os.listdir()) :
				f = os.path.join(i, 'views.py')
				ff = os.path.join(path, f)
				print('==', f, '==')
				c = read_code(open(f).read().split('\n')).tostr('')
				open(ff, 'w').write(c)
	else :
		for i in sys.argv[1:] :
			print('==', i, '==')
			print(read_code(open(i).read().split('\n')).tostr(''))


import extract
import re, os, sys, itertools, collections

def search(obj) :
	t = type(obj)
	if t == extract.bracket_tag :
		for i in search(obj.content) :
			yield i
	elif t == extract.code_list_tag :
		for i in map(search, obj.code_list) :
			for j in i :
				yield j
	elif t in (extract.code_tag, list) :
		if t == list :
			l = obj
		else :
			l = obj.word_list
		tib = extract.bracket_tag('[]')	# 'title' in bracket 略
		tib.append("'title'")
		for i in range(len(l)) :
			for j in search(l[i]) :
				yield j
			if l[i - 3: i] == ['dict_render', tib, '='] :
				c = l[i:]
				assert type(c[0]) == str
				if c and c[0][0] in '\'\"' :
					ans = eval(''.join(itertools.takewhile(
											lambda x: x[0] in '\'\"', c)))
					if '%' in ans :							# 检测模式字符串
						print(repr(ans))
					yield ans
			if l[i - 3: i] == ['Snap', '.', 'error'] or \
				l[i - 1: i] in (['Http403'], ['Http404'], 
								['error_function'], ['t_']) :
				assert l[i].symbol == '()'
				c = l[i].content
				if c and c[0][0] in '\'\"' :
					ans = eval(''.join(itertools.takewhile(
											lambda x: x[0] in '\'\"', c)))
					if l[i - 1] != 't_' and '%' in ans :	# 检测模式字符串
						print(repr(ans))
					yield ans
			if l[i - 3: i] == ['Snap', '.', 'success'] :
				assert l[i].symbol == '()'
				c = l[i].content
				assert c[:2] == ['request', ',']
				if c[2][0] in '\'\"' :
					ans = eval(''.join(itertools.takewhile(
											lambda x: x[0] in '\'\"', c[2:])))
					if '%' in ans :							# 检测模式字符串
						print(repr(ans))
					yield ans
	elif t == str :
		pass
	else :
		for i in search(obj.code) :
			yield i

def repr_po(string) :
	'Note: Unstable'
	c = string.replace('\\', r'\\').replace('\"', r'\"').replace('\n', r'\n')
	return '"%s"' % c

def read_po(lines) :
	cache = []
	for i in lines :
		if len(cache) == 0 :
			matched = re.fullmatch('msgid\s*(".*")', i)
			if matched :
				cache.append(eval(matched.groups()[0]))
				continue
		elif len(cache) == 1 :
			matched = re.fullmatch('msgstr\s*(".*")', i)
			if matched :
				cache.append(eval(matched.groups()[0]))
				continue
			matched = re.fullmatch('(".*")', i)
			if matched :
				cache[-1] += eval(matched.groups()[0])
				continue
		elif len(cache) == 2 :
			matched = re.fullmatch('(".*")', i)
			if matched :
				cache[-1] += eval(matched.groups()[0])
				continue
			else :
				yield cache
				cache = []
	if cache :	# 收尾
		assert len(cache) == 2
		yield cache

if __name__ == '__main__' :
	if sys.argv[1:] :
		for i in sys.argv[1:] :
			print(set(search(extract.read_code(open(i).read().split('\n')))))
		exit(0)
	assert os.path.exists('manage.py')
	for locale in ('en_US', 'ja_JP') :
		for i in filter(lambda x: x.startswith('quan_'), os.listdir()) :
			print('==', i, '==')
			f = os.path.join(i, 'views.py')
			folder = 'locale/%s/LC_MESSAGES/' % locale
			os.makedirs(os.path.join(i, folder), exist_ok=True)
			ff = os.path.join(i, folder, 'django.po')
			try :
				ori = list(read_po(open(ff).read().split('\n')))
			except FileNotFoundError :
				ori = []
			ori_dict = dict(ori)
			new = set(search(extract.read_code(open(f).read().split('\n'))))
			output = open(ff, 'w')
			for i in ori :
				if not i[0] :
					continue
				if i[0] not in new :
					print('# Deprecated', file=output)
				print('msgid', repr_po(i[0]), file=output)
				print('msgstr', repr_po(i[1]), file=output)
				print(file=output)
			for i in new :
				if i not in ori_dict and i :
					print('msgid', repr_po(i), file=output)
					print('msgstr', repr_po(''), file=output)
					print(file=output)
			output.close()


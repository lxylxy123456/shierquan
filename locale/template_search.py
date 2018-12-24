import extract
import re, os, sys, itertools, collections
from search import repr_po, read_po

if __name__ == '__main__' :
	assert os.path.exists('manage.py')
	for locale in sys.argv[1:] :
		assert locale in ('en_US', 'ja_JP')
		ff = 'locale/%s.po' % locale
		try :
			ori = list(read_po(open(ff).read().split('\n')))
		except FileNotFoundError :
			ori = []
		ori_dict = dict(ori)
	
		new = set()
		for app in filter(lambda x: x.startswith('quan_'), os.listdir()) :
			for p, d, f in os.walk(os.path.join(app, 'templates')) :
				for j in filter(lambda x: x.endswith('.html'), f) :
					content = open(os.path.join(p, j)).read()
					found = re.findall("{% t_ '([^\']+)' %}", content)
					new.update(found)

		output = open(ff, 'w')
		for i in ori :
			if i[0] not in new :
				print('# Deprecated', file=output)
			print('msgid', repr_po(i[0]), file=output)
			print('msgstr', repr_po(i[1]), file=output)
			print(file=output)
		for i in new :
			if i not in ori_dict :
				print('msgid', repr_po(i), file=output)
				print('msgstr', repr_po(''), file=output)
				print(file=output)
		output.close()


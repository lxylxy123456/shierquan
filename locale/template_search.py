# 
# Shierquan - a website similar to shiyiquan.net; see README.md
# Copyright (C) 2018  lxylxy123456
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# 

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


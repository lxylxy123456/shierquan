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

'读取社团申请表'

import zipfile, sys
from xml.etree import ElementTree

def rec(a, s=[], ans=[['']]) :
	'a是根结点'
	if len(s) == 4 :
		print('-' * 10)
		if ans[-1][-1] :
			ans[-1].append('')
	if len(s) == 3 :
		print('=' * 20)
		if ans[-1] != [''] :
			ans.append([''])
	if a.text and len(s) > 4 :
		for i in s :
			print(i.tag.split('}')[-1], end=' ')
		print(type(a.text))
		ans[-1][-1] += a.text
	for i in a.getchildren() :
		ans = rec(i, s + [a], ans)
	return ans

def process1(info) :
	temp1 = []
	for i in info.copy() :
		if i == [''] or i == ['总分', '赋予星级', ''] :
			continue
		if len(i) == 3 and i[:2] == ['本学期社团活动情况', '社团内部活动'] :
			i = i[1:]
		if i[-1] == '' :
			del(i[-1])
		if len(i) == 2 :
			temp1.append(i)
		elif len(i) == 4 :
			temp1.append(i[:2])
			temp1.append(i[2:])
	return dict(temp1)

def read_form(filename) :
	a = zipfile.ZipFile(filename, 'r').read('word/document.xml')
	b = ElementTree.fromstring(a)
	return process1(rec(b))

if __name__ == '__main__' :
	ans = read_form(sys.argv[1])
	for i in ans :
		print(i, ans[i], sep='\t')


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

print('''
这个程序可以批量在 views.py 中替换代码，但是由于太危险已经被禁用。将第五行删除即可启用
''')

exit(0) == int('a')

import os, sys

a = map(lambda x: x + '/views.py', filter(lambda x: x[:5] == 'quan_', 
											os.listdir('.')))
#print(sys.argv[1], sys.argv[2])
for i in a :
	s1 = sys.argv[1].encode()
	s2 = sys.argv[2].encode()
	b = s2.join(open(i, 'rb').read().split(s1))
	open(i, 'wb').write(b)

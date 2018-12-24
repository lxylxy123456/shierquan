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

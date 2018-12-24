print('''
这个程序可以批量在 models.py 中提取信息到 admin，但是由于太危险已经被禁用。
将第六行注释即可启用
''')

exit(0) == int('a')

import os, sys, re

if len(sys.argv) != 2 :
	print('请输入一个app名称')
	exit(1)

app = sys.argv[1]

assert not os.path.exists(app + '/admin.py')

env = None
name_list = []
answer = []

def export_env() :
	global env
	global name_list
	if env :
		answer.append((env, name_list))
	env = None
	name_list = []

for i in open(app + '/models.py') :
	if i.startswith('class ') :
		export_env()
		matched = re.match('class (\w+)\(models\.Model\)', i)
		if matched :
			env = matched.groups()[0]
		else :
			env = None
	elif env :
		matched = re.match('\s+(\w+)\s?=\s?models.\w+Field', i)
		if matched :
			name_list.append(matched.groups()[0])

export_env()

f = open(app + '/admin.py', 'w')
print('from django.contrib import admin', file=f)
print('from .models import *', file=f)
print(file=f)
for i, j in answer :
	print('class %s_admin(admin.ModelAdmin) :' % i, file=f)
	print('\tlist_display = %s' % repr(tuple(j)), file=f)
	print('\tsearch_fields = list_display', file=f)
	print(file=f)
for i, j in answer :
	print('admin.site.register(%s, %s_admin)' % (i, i), file=f)
print(file=f)


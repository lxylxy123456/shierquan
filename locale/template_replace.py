import os, sys, re

'''
Commands noted

p locale/template_replace.py */templates/*/*.html
p locale/template_search.py; p locale/export.py
g locale/en_US.po

'''

if __name__ == '__main__' :
	rez = '《》（），。：；“‘”’！、？'
	for f in sys.argv[1:] :
		if f.endswith('/500.html') :
			continue
		new_content = []
		if '{% load translate %}' in open(f).read() :
			continue
		for i in open(f).read().split('\n') :
			re_str = ('([\w\&\.%s][%s\s\w\&\.]*)?[\u4e00-\u9fff%s]'
					'([%s\s\w\&\.]*[%s\w\&\.])?' % ((rez, ) * 5))
			found = list(re.finditer(re_str, i))
			ans = ''
			start = 0
			for j in found :
				ans += i[start: j.start()]
				start = j.end()
				c = j.group()
				s = j.start()
				ss = i[s - 10: s]
				e = j.end()
				ee = i[e: e + 10]
				if not(ss.endswith("{% t_ '") and ee.startswith("' %}")) and \
					input(ss + '\033[41m' + c + '\033[0m' + ee) == 'y' :
					ans += "{% t_ '" + c + "' %}"
				else :
					ans += c
			ans += i[start:]
			new_content.append(ans)
		open(f, 'w').write('\n'.join(new_content))
		print('gedit', f)
		print('{% load translate %}')
		break


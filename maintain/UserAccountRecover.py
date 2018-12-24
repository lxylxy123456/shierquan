import sys
from initialize import *

def time_conv(time_str) :
	date_s, time_s = time_str.split(' ')
	y, m, d = date_s.split('-')
	s, n = time_s.split('.')
	H, M, S = s.split(':')
	N, t = n.split('+')
	return ', '.join((str(int(y)), str(int(m)), str(int(d)), str(int(H)), str(int(M)), str(int(S)), str(int(N))))

f = open(sys.argv[1])
signal = 0	# 0 begin	1 do	- end
type_dict = {
	'id': int, 
	'grade': int, 
	'phone': str, 
	'nickname': str, 
	'signature': str, 
	'status': str, 
	'time_update': datetime.datetime, 
	'time_create': datetime.datetime, 
	'pinyin': str, 
	'basic_id': User, 
}

print('from initialize import *')
for i in f.readlines():
	if i.startswith('COPY "UserAccount"') :
		signal = 1
		key_list = i.split('(')[1].split(')')[0].split(', ')
		print(key_list)
	elif i == '\.\n' and signal == 1 :
		break
	elif signal == 1 :
		val_list = i[:-1].split('\t')
		print('qry = UserAccount()')
		for i in range(len(key_list)) :
			tp = type_dict[key_list[i]]
			if tp == int :
				print('qry.%s = %s' % (key_list[i], val_list[i]))
			elif tp == str :
				print('qry.%s = "%s"' % (key_list[i], val_list[i]))
			elif tp == datetime.datetime :
				print('qry.%s = datetime.datetime(%s)' % (key_list[i], time_conv(val_list[i])))
			elif tp == User :
				print('qry.basic = User.objects.filter(id=int(%s))[0]' % (val_list[i]))
		print(
'''try :
 qry.save()
except Exception as e :
 print('error', qry.id, repr(e))
''')
print('注意不要在srva上做', file=sys.stderr)


'''
	用于翻译 obj2json.js
'''

import os, collections, sys

translate_dict = {
	'en': {
		'似乎与服务器通讯不畅': 
			'An error occurs when communicating with the server ', 
		'警告': 'Warning: ', 
		'恭喜': 'Congratulations: ', 
		'提示': 'Hint: ', 
		'跳过等待': 'Skipping', 
		'跳过: ': 'Skip: ', 
	}, 
	'ja': {
		'似乎与服务器通讯不畅': 'ネットワーク到達不能', 
		'警告': 'しまった', 
		'恭喜': 'おめでとう', 
		'提示': 'ヒント', 
		'跳过等待': '待ってない', 
		'跳过: ': 'スキップ: ', 
	}
}

if __name__ == '__main__' :
	fname = 'quan_center/static/js/obj2json.js'
	assert os.path.exists(fname)
	for i in sys.argv[1:] :
		a = open(fname).read()

		def replace(arg) :
			global a
			a = a.replace(*arg)
			print(arg)

		collections.deque(map(replace, translate_dict[i].items()), 0)
		open(fname[:-3] + '.%s.js' % i, 'w').write(a)


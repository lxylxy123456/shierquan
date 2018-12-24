import search
import re, os, sys, itertools, collections, pickle

if __name__ == '__main__' :
	assert os.path.exists('manage.py')
	for locale in sys.argv[1:] :
		assert locale in ('en', 'ja')
		ll = { 'en': 'en_US', 'ja': 'ja_JP' }[locale]
		ans = dict(filter(lambda x: x[1], 
				search.read_po(open('locale/%s.po' % ll).read().split('\n'))))
		for i in filter(lambda x: x.startswith('quan_'), os.listdir()) :
			ff = os.path.join(i, 'locale/%s/LC_MESSAGES/django.po' % ll)
			ans.update(filter(lambda x: x[1], 
								search.read_po(open(ff).read().split('\n'))))
		pickle.dump(ans, open('locale/%s.pickle' % locale, 'wb'))


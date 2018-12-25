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


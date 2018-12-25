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

from .models import *

from quan_account.views import *
from quan_auth.views import *
from quan_event.views import *
from quan_message.views import PublicMessageAction
from quan_share.views import *
from quan_ua.views import *

class NewsSnap :
	def html_script_filter(script) :
		'只允许文本编辑器的html代码通过，返回布尔值'
		low = script
		stack = []
		re1 = ('(\w+)('
				' alt="[\#\w\:\/\~\<\>\.\-\?\=\s;\']*"|'
				' class="([0-9A-Za-z\_\-]+( [0-9A-Za-z\_\-]+){0,4})?"|'
				' color="('
					'#[0-9A-Za-z\_]{0,6}|'
					'rgb\(\d{0,3}, ?\d{0,3}, ?\d{0,3}\)'
					')"|'
				' height="\d+"|'
				' href="[\#\w\:\/\~\<\>\.\-\?\=\s;\'\%]*"|'
				' rel="nofollow"|'
				' src="[\#\w\:\/\~\<\>\.\-\?\=\s;\']*"|'
				' style="('
					'margin-left: ?\d{0,2}px; ?|'
					'color: ?('
						'#[0-9A-Za-z\_]{0,6}|'
						'rgb\(\d{0,3}, ?\d{0,3}, ?\d{0,3}\)'
						');?|'
					'){0,2}"|'
				' width="\d+"'
				'){0,4}')
		re2 = '/\s?(\w+)'
		re3 = '(\w+)\s?/'
		safe_set = { 'a', 'b', 'blockquote', 'br', 'code', 'font', 'h1', 'h2', 
					'h3', 'h4', 'h5', 'h6', 'hr', 'img', 'li', 'ol', 'p', 
					'pre', 'span', 'strike', 'u', 'ul' }
		for i in low.split('<')[1:] :
			script, content = i.split('>', 1)
			if '>' in content :
				print(1)
				return False
			# <p>
			matched = re.fullmatch(re1, script)
			if matched :
				tag = matched.groups()[0]
				if tag not in safe_set :
					print(2, tag)
					return False
				if tag not in { 'br', 'hr', 'img' } :
					stack.append(tag)
				continue
			# </p>
			matched = re.fullmatch(re2, script)
			if matched :
				tag = matched.groups()[0]
				if stack.pop() != tag :
					print(3)
					return False
				continue
			# <hr />
			matched = re.fullmatch(re3, script)
			if matched :
				tag = matched.groups()[0]
				if tag not in safe_set :
					print(4)
					return False
				continue
			print(5, script)
			return False
		if stack :	# 没有正确关闭
			print(6)
			return False
		else :
			return True
	
	def news_find(tid, auto_plus=False) :
		try :
			qry = NewsInfo.objects.get(id=int(tid), status=0)
		except (ObjectDoesNotExist, MultipleObjectsReturned, ValueError) :
			return None
		if auto_plus :
			qry.visited += 1
			qry.save()
		return qry

	def news_all() :
		return NewsInfo.objects.filter(status=0).order_by('-time_update')

	def content_extract(content) :
		'返回列表'
		class NewsHTMLParser(HTMLParser):
			def __init__(self) :
				super(NewsHTMLParser, self).__init__()
				self.value = ['']
				self.tag_list = ('p', 'hr', 'blockquote', 'ol', 'li', 'br', 
								'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6')
			def handle_starttag(self, tag, attrs):
				if tag in self.tag_list :
					self.value.append('')
			def handle_endtag(self, tag):
				if tag in self.tag_list :
					self.value.append('')
			def handle_data(self, data):
				self.value[-1] += data
		parser = NewsHTMLParser()
		parser.feed(content)
		return filter(bool, parser.value)

class NewsDicts :
	def news_view(request, tid) :
		dict_render = {}
		qry = NewsSnap.news_find(tid, auto_plus=True)
		if qry == None :
			raise Http404('找不到新闻')
		dict_render['tid'] = tid
		dict_render['data'] = qry
		time_list = ChineseSnap.datetime_comp(qry.time_create)
		dict_render['time_create'] = time_list[0] + time_list[1]
		dict_render['sname'] = UserSnap.sname_find_by_uid(qry.account_id)
		dict_render['image_list'] = ShareSnap.image_list_find_by_suid \
															(qry.attach_uuid)
		print('asdf', qry.relation, qry.account_id)
		if AccountSnap.aid_verify(request, qry.relation, qry.account_id) :
			dict_render['is_auth'] = True
		return dict_render

class NewsViews :
	@vary_on_cookie
	def news_post(request) :
		dict_render = UserAgentSnap.record(request)
		if request.method == 'POST' :
			attach_uuid = request.POST.get('attach_uuid', '')
			src = request.POST.get('src', '')
			aid = request.POST.get('aid', '')
			subject = request.POST.get('subject', '')
			content = request.POST.get('content', '')
			if len(subject) <= 2 :
				raise Snap.error('请写一点标题')
			if len(content) <= 8 :
				raise Snap.error('请写一点内容')
			if len(subject) > 26 :
				raise Snap.error('标题太长')
			if len(content) > 3333 :
				raise Snap.error('内容太长')
			if not NewsSnap.html_script_filter(content) :
				raise Snap.error('包含非法字符')
			if not aid :
				raise Snap.error('找不到用户/社团')
			if not AccountSnap.aid_verify(request, src, aid) :
				raise Snap.error('冒充别人')
			nid = request.POST.get('nid', '')
			if nid != '' :	# 更改
				tid = int(nid)
				qry = NewsSnap.news_find(tid)
				if qry == None :
					raise Snap.error('无法找到更改项目')
				if qry.relation != src or qry.account_id != int(aid) :
					raise Snap.error('不是新闻作者')
				qry.subject = subject
				qry.content = content
				qry.save()
			else :			# 发布
				if attach_uuid != '':
					if not ShareSnap.attach_find_by_uuid(attach_uuid).exists() :
						raise Snap.error('无法找到这个AttachID')
				qry = NewsInfo(subject=subject, content=content, relation=src, 
						account_id=aid, attach_uuid=attach_uuid)
				qry.save()
				PublicMessageAction.save(request, 'news', 'new', 
										aid, src, qry.id, 'news')
			return Snap.success(request, '投递成功', 
								{ 'redirect': '/news/%d/' % qry.id })
		else :
			tid = request.GET.get('nid', '')
			dict_render['src'] = request.GET.get('src', '')
			dict_render['aid'] = request.GET.get('aid', '')
			dict_render['title'] = ' - 发表新闻'
			if tid != '' :
				dict_render['title'] = ' - 编辑新闻'
				dict_render['nid'] = tid
				qry = NewsSnap.news_find(int(tid))
				if qry == None :
					raise Http404('找不到对象')
				aid = qry.account_id
				src = qry.relation
				dict_render['aid'] = aid
				dict_render['src'] = src
				if qry.relation != src or qry.account_id != int(aid) or \
					not AccountSnap.aid_verify(request, src, int(aid)) :
					raise Http403('不是新闻作者')
				dict_render.update(NewsDicts.news_view(request, int(tid)))
			return Snap.render('news_post.html', dict_render)

	@vary_on_cookie
	def news_view(request, tid) :
		dict_render = UserAgentSnap.record(request)
		dict_render.update(NewsDicts.news_view(request, tid))
		dict_render['title'] = t_(' - %s') % dict_render['data'].subject
		return Snap.render('news_view.html', dict_render)

	@vary_on_cookie
	def news_delete(request, tid) :
		dict_render = UserAgentSnap.record(request)
		if request.method == 'POST' :
			qry = NewsSnap.news_find(int(tid))
			if qry == None :
				raise Snap.error('无法找到更改项目')
			aid = qry.account_id
			src = qry.relation
			if qry.relation != src or qry.account_id != int(aid) or \
				not AccountSnap.aid_verify(request, src, int(aid)) :
				raise Snap.error('不是新闻作者')
			qry.status = 1
			qry.save()
			return Snap.success(request, '成功删除', { 'redirect': '/news/' })
		else :
			return Snap.redirect('/news/%s/' % tid)

	@vary_on_cookie
	def news_list(request) :
		dict_render = UserAgentSnap.record(request)
		qry = NewsSnap.news_all()
		sliced_qry = AuthDicts.page_dict(request, qry, 10, dict_render)
		dict_render['news_list'] = []
		for i in sliced_qry :
			image_list = ShareSnap.image_list_find_by_suid(i.attach_uuid)
			if image_list :
				image = image_list[0]
			else :
				image = None
			dict_render['news_list'].append({
				'data': i, 
				'date': ChineseSnap.datetime_simp(i.time_create), 
				'prompt': ' '.join(NewsSnap.content_extract(i.content))[:30], 
				'image': image, 
			})
		dict_render['title'] = ' - 新闻'
		return Snap.render('news_list.html', dict_render)

class NewsSiteMap(Sitemap) :
	def items(self) :
		return NewsInfo.objects.filter(status=0)
	def location(self, item) :
		return '/news/%d/' % item.id


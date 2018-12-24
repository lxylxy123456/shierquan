from .models import *

from quan_forum.models import *

from quan_account.views import *
from quan_message.views import PublicMessageAction
from quan_ua.views import *

class AvatarSnap :
	def avatar_find(src, aid, size='', none=False) :
		'''
			取得某个大小的头像
			size in ('large', 'medium', 'small', 'raw')"
		'''
		answer = AvatarSnap.avatar_all(src, aid, none)
		if none :
			if not answer :
				return None
		if size not in answer :
			size = 'raw'
		return answer[size]

	def avatar_all(src, aid, none=False) :
		'''
			取得头像，返回大中小
		'''
		cache_key = 'AvatarSnap__avatar_all__%s_%d' % (src, aid)
		cached = cache.get(cache_key)
		if cached == 'not found' :
			if none :
				return None
			return {
				'large': '/static/images/large/avatar-%s-default.png' % src, 
				'medium': '/static/images/medium/avatar-%s-default.png' % src, 
				'small': '/static/images/small/avatar-%s-default.png' % src, 
				'raw': '/static/images/avatar-%s-default.png' % src, 
			}
		if cached :
			return cached
		try :
			name = AvatarAccount.objects.filter(account_id=aid, 
							relation=src).order_by('-time_update').first().name
			answer = {
				'large': '/media/images/avatar/large/' + name, 
				'medium': '/media/images/avatar/medium/' + name, 
				'small': '/media/images/avatar/small/' + name, 
				'raw': '/media/images/avatar/' + name, 
			}
			cache.set(cache_key, answer, random.randint(800000, 900000))
			return answer
		except AttributeError :
			cache.set(cache_key, 'not found', random.randint(800000, 900000))
			if none :
				return None
			return {
				'large': '/static/images/large/avatar-%s-default.png' % src, 
				'medium': '/static/images/medium/avatar-%s-default.png' % src, 
				'small': '/static/images/small/avatar-%s-default.png' % src, 
				'raw': '/static/images/avatar-%s-default.png' % src, 
			}

	def crop(im, src, aid, name, temp_name) :
		'裁剪头像'
		length = min(im.size)
		left = (im.size[0] - length) // 2
		top = (im.size[1] - length) // 2
		path = os.path.join(settings.MEDIA_ROOT, 'images', 'avatar', name)
		im_cropped = im.crop((left, top, left + length, top + length))
		im_cropped.thumbnail( (320, 320) )
		im_cropped.save(path)
		AvatarAccount(relation=src, account_id=aid, name=name, 
					temp_name=temp_name).save()
		
	def temp_name_get(origin_name) :
		'通过时间和后缀计算临时文件名称'
		suffix = origin_name.rsplit('.', 1)[-1]
		time_str = datetime.now().strftime('%F&%H+%M+%S&%f')
		return '%s&%d.%s' % (time_str, random.randint(0, 100), suffix)

	def avatar_make(name) :
		'''
			将
				media/images/avatar/name
			计算为
				media/images/avatar/[大小]/name
			的文件
			由于之前已经进行 320 * 320 的裁减了，所以省略了很多算法
		'''
		path = os.path.join(settings.MEDIA_ROOT, 'images', 'avatar', name)
		im = Image.open(path)
		for i, j in ((128, 'large'), (64, 'medium'), (32, 'small')) :
			im.thumbnail((i, i))
			path = os.path.join(settings.MEDIA_ROOT, 'images/avatar', j, name)
			im.save(path)

class AvatarViews :
	@vary_on_cookie
	def avatar_upload(request, src, sname):
		dict_render = UserAgentSnap.record(request)
		dict_render['upload_url'] = '/avatar/%s/%s/' % (src, sname)
		if src == 'club' :
			real_name = ClubSnap.alias_find_by_sname(sname)
			if real_name != sname and real_name :
				return Snap.redirect('/avatar/club/%s/' % real_name)
			if not real_name :
				raise Http404()
		if src == 'forum' :
			from quan_forum.views import ForumSnap
			gid = ForumSnap.gid_find_by_sname(sname)
			if not ForumSnap.group_admin_verify(request, gid) :
				raise Http403('您没有权限')
		else :
			if AccountSnap.sname_verify(request, src, sname) == False :
				raise Http403('您没有权限')
		dict_render['home_link'] = '/%s/%s/' % (src, sname)
		if src == 'club' :
			aid = AccountSnap.aid_find_by_sname(src, sname)
			dict_render['full_name'] = ClubSnap.fname_find_by_cid(aid)
			dict_render['object_name'] = t_('社团')
		elif src == 'user' :
			dict_render['full_name'] = request.user.first_name
			dict_render['object_name'] = t_('用户')
		elif src == 'forum' :
			dict_render['full_name'] = ForumSnap.fname_find_by_gid(gid)
			dict_render['object_name'] = t_('论坛')
		else :
			dict_render['full_name'] = request.user.first_name
		dict_render['title'] = t_(' - 上传%s头像') % dict_render['object_name']
		if request.method != 'POST' :
			return Snap.render('avatar_add.html', dict_render)
		# 开始处理 POST 的情况

		def error_function(content) :
			dict_render['content'] = t_(content)
			return Snap.render('avatar_add.html', dict_render)

		if 'image' not in request.FILES :
			return error_function('似乎没选择任何文件？')
		img_file = request.FILES['image']
		temp_name = AvatarSnap.temp_name_get(img_file.name)
		temp_path = os.path.join(settings.MEDIA_ROOT, 'images', 
								'temp', temp_name)
		if img_file.size > 1800000:
			return error_function('这个文件过大[已抛弃]')
		try:
			file_token = open(temp_path, 'wb')
			for chunk in img_file.chunks() :
				file_token.write(chunk)
			file_token.close()
		except Exception as e:
			return error_function('出现了一个神秘的错误')
		try:
			im = Image.open(temp_path)
		except OSError as e:
			return error_function('你确定是在上传图片？')
		name = src + '-' + sname + ".png"
		aid = AccountSnap.aid_find_by_sname(src, sname)
		if im.size[0] < 320 or im.size[1] < 320 :
			return error_function('您的头像朱军画质，像素渣渣')
		try :
			AvatarSnap.crop(im, src, aid, name, temp_name)
		except Exception as e :
			return error_function('很抱歉，您的头像格式无法被处理')
		try :
			AvatarSnap.avatar_make(name)
		except Exception as e :
			return error_function('一个神秘的错误出现了')
		if src in ('club', 'user') :
			PublicMessageAction.save(request, src, 'avatar', aid, src)
		CacheSnap.avatar_uploaded(src, sname)
		return Snap.success(request, '头像更新成功', 
							{ 'redirect': '/%s/%s/' % (src, sname) })


#!/usr/bin/env python3
import os, sys, django, socket
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shierquan.settings")
django.setup()
from django.conf import settings
from quan_account.views import *
from quan_auth.views import *
from quan_avatar.views import *
from quan_badge.views import *
from quan_center.views import *
from quan_event.views import *
from quan_email.views import *
from quan_forum.views import *
from quan_forum_old.views import *
from quan_news.views import *
from quan_message.views import *
from quan_mobile.views import *
from quan_share.views import *
from quan_square.views import *
from quan_ua.views import *

def mkdir(dir_name) :
	try :
		os.mkdir(dir_name)
	except FileExistsError :
		print('exist:\t%s' % dir_name)
	if socket.gethostname() != 'laptop' :
		os.system('chown www-data:www-data -R %s' % dir_name)

def create_testing_database() :
	assert not User.objects.count()
	app_list = (filter(lambda x: re.search('^quan_', x), 
						settings.INSTALLED_APPS))
	for i in app_list :
		try :
			a = map(lambda x: re.search('^class (\w+)', x).groups()[0], 
				filter(lambda x: re.search('^class \w+\s*\(models.Model\)', x), 
					open(i + '/models.py').readlines()))
		except FileNotFoundError :
			continue
		assert not any(map(lambda x: eval(x).objects.count(), a))
	# 以上确保没有任何数据库中包含东西
	def add_user(s, f) :
		a = User(username='%s@%s.%s' % (s,s,s), first_name=f, last_name=s)
		a.set_password(s); a.save()
		qry = UserAccount(basic=a, phone='12345678901', grade=6, 
						nickname=s+'昵称', signature=s+'签名')
		qry.save()
		return qry.id
	def add_club(s, owner) :
		qry = ClubAccount(full_name=s+'全称', simp_name=s, category='other', 
						simp_intro=s+'简介', full_intro=s+'详细介绍', pinyin=s)
		qry.save()
		AccountRelation(account_id_B=qry.id,account_id_A=owner,relation='head')
		return qry.id
	def add_event(s, c, t1, t2) :
		t = lambda x: datetime.now() + timedelta(0,x * 3600,0)
		qry = EventInfo(subject=s+'标题', content=s+'内容', account_id=c, 
						relation='club', time_set=t(t1), time_end=t(t2))
		qry.save()
		return qry.id
	def add_share(s, c, category) :
		qry = ShareInfo(subject=s+'标题', content=s+'内容', account_id=c, 
						relation='club', attach_uuid=ShareSnap.uuid_create(), 
						category=category)
		qry.save()
		return qry.id, qry.attach_uuid
	u1 = add_user('jkl', 'あ')	# 用 jkl@jkl.jkl 和 jkl 登录
	u2 = add_user('uio', 'い')
	u3 = add_user('asdf', 'う')
	u4 = add_user('qwer', 'え')
	c1 = add_club('hcc', u1)
	c2 = add_club('club-union', u1)
	c3 = add_club('jkl', u1)
	c4 = add_club('uio', u1)
	AccountRelation(account_id_B=c1, account_id_A=u1, relation='head').save()
	AccountRelation(account_id_B=c2, account_id_A=u1, relation='head').save()
	AccountRelation(account_id_B=c3, account_id_A=u1, relation='head').save()
	AccountRelation(account_id_B=c4, account_id_A=u1, relation='head').save()
	AccountRelation(account_id_B=c1, account_id_A=u2, relation='vice').save()
	AccountRelation(account_id_B=c2, account_id_A=u2, relation='vice').save()
	AccountRelation(account_id_B=c3, account_id_A=u2, relation='core').save()
	AccountRelation(account_id_B=c4, account_id_A=u2, relation='core').save()
	AccountRelation(account_id_B=c1, account_id_A=u3, relation='member').save()
	AccountRelation(account_id_B=c2, account_id_A=u3, relation='member').save()
	AccountRelation(account_id_B=c3, account_id_A=u3, relation='member').save()
	AccountRelation(account_id_B=c4, account_id_A=u3, relation='member').save()
	e1 = add_event('活动1', c1, -8, -7)
	e2 = add_event('活动2', c1, -6, -5)
	e3 = add_event('活动3', c1, -4, -3)
	e4 = add_event('活动4', c1, -2, -1)
	e5 = add_event('活动5', c1,  0,  1)
	EventQuest(event_id=e1, answer='n1', quest='q1', option_A='a1', 
				option_B='b1', option_C='c1', token=1).save()
	EventQuest(event_id=e3, answer='n3', quest='q3', option_A='a3', 
				option_B='b3', option_C='c3', token=123).save()
	EventQuest(event_id=e5, answer='n5', quest='q5', option_A='a5', 
				option_B='b5', option_C='c5', token=12345).save()
	EventRelation(account_id=u2,relation='signup',event_id=e1,status='success')
	EventRelation(account_id=u2,relation='signup',event_id=e3,status='success')
	EventRelation(account_id=u3,relation='signup',event_id=e3,status='success')
	EventRelation(account_id=u3,relation='signup',event_id=e5,status='success')
	EventRelation(account_id=u4,relation='nice',event_id=e1,status='success')
	EventRelation(account_id=u4,relation='nice',event_id=e2,status='success')
	EventRelation(account_id=u4,relation='nice',event_id=e3,status='success')
	EventRelation(account_id=u4,relation='nice',event_id=e4,status='success')
	EventRelation(account_id=u4,relation='nice',event_id=e5,status='success')
	s1, ss1 = add_share('e1', c1, 'event')
	s2, ss2 = add_share('h2', c1, 'handout')
	s3, ss3 = add_share('k3', c2, 'knowledge')
	s4, ss4 = add_share('e4', c3, 'event')
	s5, ss5 = add_share('e5', c4, 'event')
	ShareEventRelation(share_id=s1, event_id=e1).save()
	ShareEventRelation(share_id=s2, event_id=e2).save()
	ShareEventRelation(share_id=s3, event_id=e3).save()
	uuf = 'uu-friend'
	AccountRelation(account_id_B=u1, account_id_A=u2, relation=uuf).save()
	AccountRelation(account_id_B=u1, account_id_A=u3, relation=uuf).save()
	AccountRelation(account_id_B=u2, account_id_A=u3, relation=uuf).save()
	# Snap for dev
	# drop database postgres; create database postgres;

if __name__ == "__main__":
	if input("1.	Create directories? [y/N]") == 'y' :
		mkdir('%s' % settings.MEDIA_ROOT)
		mkdir('%sfiles/' % settings.MEDIA_ROOT)
		mkdir('%simages/' % settings.MEDIA_ROOT)
		mkdir('%simages/avatar/' % settings.MEDIA_ROOT)
		mkdir('%simages/avatar/large/' % settings.MEDIA_ROOT)
		mkdir('%simages/avatar/medium/' % settings.MEDIA_ROOT)
		mkdir('%simages/avatar/small/' % settings.MEDIA_ROOT)
		mkdir('%simages/qrcode/' % settings.MEDIA_ROOT)
		mkdir('%simages/temp/' % settings.MEDIA_ROOT)
		mkdir('%simages/share/' % settings.MEDIA_ROOT)
		mkdir('%simages/share/exlarge/' % settings.MEDIA_ROOT)
		mkdir('%simages/share/large/' % settings.MEDIA_ROOT)
		mkdir('%simages/share/medium/' % settings.MEDIA_ROOT)
		mkdir('%simages/share/small/' % settings.MEDIA_ROOT)
		mkdir('%sarchives/' % settings.MEDIA_ROOT)
		mkdir('%sarchives/batch/' % settings.MEDIA_ROOT)
		mkdir('%sarchives/funds/' % settings.MEDIA_ROOT)
		mkdir('%sforms/' % settings.MEDIA_ROOT)
		mkdir('%sforms/funds/' % settings.MEDIA_ROOT)
		mkdir('%sstream/' % settings.MEDIA_ROOT)
	if input('2.	Initialize qrcode files? [y/N]') == 'y' :
		QrcodeSnap.qrcode_init()
	if input('3.	Initialize real name database? [y/N]') == 'y' :
		UserAgentSnap.initialize(fix=1)
	if input('12.	Increase students\' grade? [y/N]') == 'y' :
		content = str(datetime.now().microsecond)
		if input('输入以下字符来确认 %s : ' % content) == content :
			for i in (6, 5, 4, 3, 2, 1) :
				UserAccount.objects.filter(grade=i).update(grade=i+1)
	if input('13.	Initialize size information of ShareAttach? [y/N]') == 'y' :
		ShareSnap.size_calc(ShareAttach.objects.all())
	if input('16.	Commit initial migrations? [y/N]') == 'y' :
		os.system('python3 manage.py makemigrations quan_*')
		os.system('python3 manage.py migrate')
	if input('17.	Create testing database information? [y/N]') == 'y' :
		c1, c2 = datetime.now().microsecond, random.randint(0, 10 ** 6)
		print('请确保数据库中没有任何记录，请绝对不要在生产服务器上执行这条命令')
		assert 'HCCSERVER' not in socket.gethostname()
		if int(input('计算 %d + %d 以确认: ' % (c1, c2))) == c1 + c2 :
			print('开始执行')
			create_testing_database()
			print('执行完毕')
		else:
			print('数据计算错误')

if 0 and '以下是已经被归档的功能，不建议使用' :
	if input("4.	Initialize students' grades? [y/N]") == 'y' :
		UserAgentSnap.grade_adhere()
	if input("5.	Truncate simple introductions? [y/N]") == 'y' :
		ClubSnap.intro_truncate()
	if input("6.	Calculate thumbnailed pictures? [y/N]") == 'y' :
		for i in os.walk(os.path.join(settings.MEDIA_ROOT, 'images', 
			'avatar')).__next__()[2] :
			try :
				AvatarSnap.avatar_make(i)
			except OSError :
				print('OSError at %s' % (i))
	if input("7.	Calculate mixed pictures? [y/N]") == 'y' :
		qry = AccountSnap.club_all_find()
		for i in qry :
			try :
				ShareSnap.mix_create(i.id)
			except OSError :
				print('OSError at club(id=%d, sname=%s)' % (i.id, i.simp_name))
	if input('8.	Thumbnail share pictures? [y/N]') == 'y' :
		for i in ShareAttach.objects.filter(category='image') :
			try :
				sname = AccountSnap.sname_find(i.relation, i.account_id)
				ShareSnap.share_thumbnail(sname, i.name_new)
				print('success:\t[%s][%s]' % (i.attach_uuid, i.second_uuid))
			except Exception as e :
				print('error:\t[%s][%s]\t%s\t%s' % \
					(i.attach_uuid, i.second_uuid, str(type(e)), str(e)))
	if input('9.	Archive share files? [y/N]') == 'y' :
		for i in ShareInfo.objects.filter(status=0) :
			comment = ShareSnap.archive_create(i.attach_uuid)
			if comment[0] :
				print('error:\t%s\t%s' % \
					(i.attach_uuid, comment[1]))
			else :
				print('success:\t%s\t%s' % (i.attach_uuid, comment[1]))
	if input('10.	Initialize pinyin? [y/N]') == 'y' :
		for i in UserAccount.objects.all() :
			i.pinyin = ''.join(pypinyin.lazy_pinyin(i.basic.first_name))
			i.save()
		for i in ClubAccount.objects.all() :
			i.pinyin = ''.join(pypinyin.lazy_pinyin(i.full_name))
			i.save()
	if input('11.	Calculate hash in UpdateStatus? [y/N]') == 'y' :
		for i in UpdateStatus.objects.all() :
			if not i.hash_value :
				i.hash_valud = hash(i.content)
				i.save()
	if input('14.	Create stream for ShareAttach? [y/N]') == 'y' :
		for i in ShareAttach.objects.filter(video_status=1) :
			ShareSnap.stream_thumbnail(i)
			i.save()
			print(i.id, i.name_new, i.name_raw, sep='\t')
	if input('15.	Thumbnail share videos? [y/N]') == 'y' :
		for i in ShareAttach.objects.filter(video_status=0) :
			try :
				ShareSnap.share_thumbnail(True, i.name_new)
				print('success:', i.name_new)
			except Exception as e :
				print('error:\t[%s][%s]\t%s\t%s' % \
					(i.attach_uuid, i.second_uuid, str(type(e)), str(e)))
	if input('18.	Calculate visitors for accounts? [y/N]') == 'y' :
		vcbs = UserAgentSnap.visit_count_by_sname
		print('Calculating Users ', datetime.now())
		for index, i in enumerate(UserAccount.objects.all()) :
			print(index, 'user', i.basic.last_name, sep='\t')
			i.visitors = vcbs('user', i.basic.last_name)
			i.save()
		print('Calculating Clubs ', datetime.now())
		for index, i in enumerate(ClubAccount.objects.all()) :
			print(index, 'club', i.simp_name, sep='\t')
			i.visitors = vcbs('club', i.simp_name)
			i.save()
		print('Calculating Events', datetime.now())
		for index, i in enumerate(EventInfo.objects.all()) :
			print(index, 'event', i.id, sep='\t')
			i.visitors = vcbs('event', i.id)
			i.save()
		print('Done')


from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

handler404 = 'defaults.page_not_found'
handler500 = 'defaults.server_error'
handler403 = 'defaults.permission_denied'
handler400 = 'defaults.bad_request'

admin.site.site_header = '十二圈后台'
admin.site.index_title = '站点管理'

urlpatterns = [
    # Examples:
    # url(r'^$', 'shiyiquan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^static/(?P<path>.*)$', serve, settings.STATIC_DICT),
    url(r'^media/(?P<path>.*)$', serve, settings.MEDIA_DICT),

    url(r'^', include('quan_account.urls')),
    url(r'^', include('quan_center.urls')),
    url(r'^', include('quan_email.urls')),
    url(r'^', include('quan_square.urls')),
    url(r'^', include('quan_news.urls')),
    url(r'^', include('quan_ua.urls')),

    url(r'^auth/',include('quan_auth.urls')),
    url(r'^avatar/', include('quan_avatar.urls')),
    url(r'^badge/',include('quan_badge.urls')),
    url(r'^event/', include('quan_event.urls')),
    url(r'^message/',include('quan_message.urls')),
    url(r'^share/',include('quan_share.urls')), 
    url(r'^mobile/',include('quan_mobile.urls')), 
    url(r'^forum/', include('quan_forum.urls')), 
    url(r'^forum-old/', include('quan_forum_old.urls')), 

    url(r'^admin/', include(admin.site.urls)),
]


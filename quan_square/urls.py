from django.conf.urls import *
from .views import *

urlpatterns = [
    url(r'^$', SquareViews.home_view),
    url(r'^wall/$', SquareViews.wall_view),
    url(r'^search/$', SquareViews.search_view),
    url(r'^search/(event)/$', SquareViews.search_view),
    url(r'^search/(share)/$', SquareViews.search_view),
    url(r'^guide/$', SquareViews.guide_view),
    url(r'^square/$', SquareViews.event_all),
    url(r'^square/relative/$', SquareViews.event_all),
    url(r'^square/hotest/$', SquareViews.event_all),
    url(r'^square/club/$', SquareViews.club_all),
    url(r'^square/club/fetch/$', SquareViews.club_fetch),
    url(r'^home/note-read/$', SquareViews.note_read),
    url(r'^random/$', SquareViews.club_random),
]

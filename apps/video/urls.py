#__author__ = 'tqn'
from django.conf.urls import *
from .views import VideoDetailView, VideoListView

urlpatterns = patterns('apps.video.views',
   url(r'list/$', VideoListView.as_view(), name='my-videos'),
   url(r'list/(?P<user_id>\d+)/$', VideoListView.as_view(), name='videos-list-of-user'),
   url(r'^(?P<pk>\d+)/$', VideoDetailView.as_view(), name='video-detail'),
)


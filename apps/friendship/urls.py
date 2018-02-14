#__author__ = 'Tam'
from django.conf.urls import *
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('apps.friendship.views',
    url(r'^request/$', 'request_friend'),
)

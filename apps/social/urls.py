__author__ = 'Administrator'
from django.conf.urls import *
from .views import *

urlpatterns = patterns('apps.social.views',
                       url(r'^getuser/$', 'get_user', name='get_user'))




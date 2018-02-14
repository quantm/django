#__author__ = 'Tam'
from django.conf.urls import *
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('apps.customer.views',
    url(r'^profile/(?P<user_id>\d+)/$', login_required(ViewUserProfile.as_view()), name='view_user_profile'),
    url(r'ajax-upload-avatar', 'ajax_upload_avatar'),
    url(r'crop-avatar', 'crop_avatar'),
)


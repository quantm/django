#__author__ = 'tqn'
from compressor.utils.stringformat import selftest
from django.conf.urls import *

urlpatterns = patterns('apps.bookmarklet.views',
   url(r'form', 'bookmark_let_form', name='bookmark-let-form'),
   url(r'save', 'bookmark_let_post', name='bookmark-let-post-link'),
)


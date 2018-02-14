# Create your views here.

import json
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse
from .forms import *
from django.contrib.auth.models import User
from apps.products.views import save_product
from apps.video.views import save_video


def bookmark_let_form(request):
    frm_bookmark_let = BookmarkLetForm
    return render_to_response('bookmarklet/bookmark_let_form.html',
                              {
                                  'page_title': 'Bookmark Let Form',
                                  'user': User.objects.all(),
                                  'frm_bookmark_let': frm_bookmark_let
                              }, context_instance=RequestContext(request))


def bookmark_let_post(request):
    if request.method == "POST" and request.is_ajax():

        message = {
            'code': 0,
            'pro_link': '',
            'back_text': u'Back',
            'mes_box': u'<h1>The info invalid</h1>',
        }

        bookmark_let_form = BookmarkLetForm(request.POST or None)
        if bookmark_let_form.is_valid():
            if(request.POST['video_code'] == u'null'):
                message = save_product(request)
            else:
                message = save_video(request)

    else:
        message = {'msg': "GET petitions are not allowed for this view."}

    return HttpResponse(json.dumps(message))

from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response


def get_user(request):
    return render_to_response('social/user.html',
                              {
                                'user': User.objects.all(),
                                'arr_length':User.objects.all().__len__()
                              }, context_instance=RequestContext(request))
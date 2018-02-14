# Create your views here.

import os, urllib, time, hashlib, cStringIO, PIL.Image as Image, string
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from oscar.core.utils import slugify
from oscar.apps.customer.mixins import PageTitleMixin

from settings import MEDIA_ROOT, VIDEO_THUMB
from .forms import VideoForm
from .models import Video


def save_video(request):
    video_form = VideoForm(request.POST or None)
    if video_form.is_valid():
        title = request.POST['title']
        video_slug = slugify(title)
        video_code = request.POST['video_code']
        description = request.POST['description']
        user = request.user
        trending = request.POST['video_is_trending']
        image_url_from_web = urllib.unquote(request.POST['image']).decode('utf8')
        url_thumb = render_thumb_path(image_url_from_web)
        save_thumb(image_url_from_web, url_thumb)
        video = Video(title=title, slug=video_slug, url=video_code, thumb=url_thumb, description=description, user=user, is_trending=trending)
        video.save()

        video_link = "/video/%s/" % video.pk
        return {
            'code': 1,
            'pro_link': u'<a href="%s" class="f-button close" target="_blank">%s</a>' % (video_link, u'See the video'),
            'back_text': u'Add more Videos',
            'mes_box': u'<h1>Video has been saved!</h1>',
        }


def save_thumb(image_url_from_web, url_thumb):
    #need recheck MEDIA_ROOT was configured in settings file
    try:
        image_on_web = urllib.urlopen(image_url_from_web)
        if image_on_web.headers.maintype == 'image':
            buf = image_on_web.read()
            #to check dirs
            arr_path = os.path.split(MEDIA_ROOT + url_thumb)
            if not os.path.exists(arr_path[0]):
                os.makedirs(arr_path[0])

            downloaded_image = file(MEDIA_ROOT + url_thumb, "wb")
            downloaded_image.write(buf)

            downloaded_image.close()
            image_on_web.close()
        else:
            return False
    except:
        return False
    return True

def render_thumb_path(image_url_from_web):
    io_file = cStringIO.StringIO(urllib.urlopen(image_url_from_web).read())
    img_file = Image.open(io_file)

    image_extension = '.' + string.lower(img_file.format)
    image_name = hashlib.md5(b'%s' % time.time()).hexdigest() + image_extension
    path_image = VIDEO_THUMB + image_name

    if os.path.exists(MEDIA_ROOT + path_image):
        path_image = VIDEO_THUMB + hashlib.md5(b'%s' % time.time()).hexdigest() + image_extension

    return path_image

class VideoDetailView(PageTitleMixin, DetailView):
    context_object_name = active_tab = "my-videos"
    page_title = ''
    model = Video

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        current_video = Video.objects.get(pk=self.kwargs['pk'])
        context['videos'] = Video.objects.filter(user=current_video.user).exclude(pk=self.kwargs['pk'])

        return context

class VideoListView(PageTitleMixin, ListView):
    context_object_name = active_tab = "my-videos"
    page_title = _('My Videos')
    model = Video

    def get_context_data(self, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        user = self.request.user
        if 'user_id' in self.kwargs.keys():
            if self.kwargs['user_id'].isnumeric():
                user = User.objects.get(pk=self.kwargs['user_id'])
        qs = Video.objects.filter(user=user).order_by('-view', 'create')
        return qs
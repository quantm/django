from django.db import models
from django.db.models import permalink
from oscar.core.utils import slugify
from django.contrib.auth.admin import User
from django.utils.translation import ugettext_lazy as _

from settings import VIDEO_THUMB

# Create your models here.

VIDEO_OPTIONS = (
    ('0', u'To My Videos'),
    ('1', u'To trending'),
)

STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
    ('e', 'Deleted'),
)

class Video(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=False)
    url = models.CharField(_('Video Code'), max_length=255)#if using youtube website, it will store video code
    thumb = models.ImageField(_('Thumbnail'), upload_to=VIDEO_THUMB,
                              max_length=255, blank=True, null=True, default='')
    description = models.TextField(_('Description'), null=True)
    user = models.ForeignKey(User)
    create = models.DateTimeField(auto_now_add=True, editable=False)
    view = models.IntegerField(max_length=128, blank=True, default=0)
    like = models.IntegerField(max_length=128, blank=True, default=0)
    is_trending = models.IntegerField(blank=True, default=0, choices=VIDEO_OPTIONS)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="p")

    def __unicode__(self):  # Python 3: def __str__(self):
        return u'%s %s' % (self.title, self.description)

    @permalink
    def get_absolute_url(self):
        return ("video-detail", None, {'title_slug': slugify(self.title), 'video_pk':self.pk})

    class Meta:
        db_table = u'video'


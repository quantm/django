import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractProductImage
from django.contrib.auth.models import User


class Product(AbstractProduct):
    user = models.ForeignKey(User, blank=True, null=True)
    is_trending = models.IntegerField(blank=True, default=0, null=True)


class ProductImage(AbstractProductImage):
    none_watermark = models.ImageField(_("Image none watermark"), upload_to=settings.OSCAR_IMAGE_FOLDER,
                                               max_length=255, blank=True, null=True, default='',
       help_text=_("""An image has a copy none watermark to using in collection view function"""))

from oscar.apps.catalogue.models import *

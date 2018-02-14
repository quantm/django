#__author__ = 'tqn'
from settings import SITE_ID
from django.db.models.signals import post_save
from django.dispatch import receiver
from oscar.apps.catalogue.models import ProductImage
from django.contrib.sites.models import Site

#Using for wartermark app
import os, urllib, cStringIO, datetime
from PIL import Image, ImageFont, ImageDraw
from settings import *

@receiver(post_save, sender=ProductImage)
def make_wartermark_for_image(sender, instance=None, created=False, **kwargs):
    if instance.original:
        if kwargs['update_fields'] is None or 'none_watermark' not in kwargs['update_fields']:
            #get site setting
            site = Site.objects.get(id__exact=SITE_ID)
            #keep image path none watermark
            keep_image_path = instance.original.name
            file_ext = os.path.splitext(keep_image_path)
            file_nm = hash(os.path.basename(file_ext[0]))
            new_image_path = datetime.datetime.now().strftime(OSCAR_IMAGE_FOLDER) + ('%d' % file_nm) + file_ext[1]
            #get old image
            get_image = Image.open(instance.original.path)
            get_image.save(os.path.abspath(MEDIA_ROOT + new_image_path))

            default_logo_to_watermark = site.name + WATERMARK_LOGO
            file = cStringIO.StringIO(urllib.urlopen(default_logo_to_watermark).read())
            logo = Image.open(file)
            logo_w, logo_h = logo.size
            #Set position to put text on the image
            text_position = (16, logo_h + 32)
            #load font for text
            font = ImageFont.truetype(FONT_PATH , WATERMARK_TEXT_FONT_SIZE)

            #Get image file from data
            image_file = instance.original
            path_to_save = image_file.path
            file_url = os.path.abspath(path_to_save)

            #Read image file from data
            background = Image.open(file_url)
            bg_w, bg_h = background.size
            #
            draw = ImageDraw.Draw(background)
            #Put text on the image

            draw.text(text_position, WATERMARK_TEXT, font=font, fill=int(WATERMARK_TEXT_COLOR))

            #Check site image and logo
            if (bg_w <= logo_w) or (bg_h <= logo_h):
                new_size = (bg_w/4-16, bg_h/4-16)
                logo = logo.resize(new_size, Image.ANTIALIAS)
            elif (bg_w-logo_w) < 16 or (bg_h-logo_h) < 16:
                new_size = (logo_w/2-16, logo_h/2-16)
                logo = logo.resize(new_size, Image.ANTIALIAS)

            #put logo on the image
            background.paste(logo, WATERMARK_LOGO_POSITION, logo)
            background.save(path_to_save)
            product_image = instance
            if hasattr(product_image, 'none_watermark'):
                product_image.none_watermark = new_image_path
                product_image.save(update_fields=['none_watermark'])
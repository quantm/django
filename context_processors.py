# import the settings file
from settings import *
from django.conf import settings
from django.contrib.sites.models import Site


def settings_values(request):
    # return the value you want as a dictionary. you may add multiple values in there.
    site = Site.objects.get(id__exact=SITE_ID)

    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'

    return {
        'DISPLAY_NAME': site.name,
        'DOMAIN_NAME': site.domain,
        'STATIC_JS_URL': STATIC_JS_URL,
        'STATIC_CSS_URL': STATIC_CSS_URL,
        'FORM_URL': FORM_URL,
        'INIT_BOOKMARKLET_FILE': INIT_BOOKMARKLET_FILE,
        'BOOKMARKLET_CSS_FILE': BOOKMARKLET_CSS_FILE,
        'BOOKMARKLET_SAVE_FILE': BOOKMARKLET_SAVE_FILE,
        'BASE_URL': scheme + request.get_host(),
    }


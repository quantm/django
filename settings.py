# Django settings for testing project.
import os.path
import sys
from oscar.defaults import *
from oscar import get_core_apps
from oscar import OSCAR_MAIN_TEMPLATE_DIR
from lib.braintree import Configuration, Environment
from django.utils.translation import ugettext_lazy as _
import djcelery
djcelery.setup_loader()

PROJECT_ROOT = os.path.dirname(__file__)
location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)


DEBUG = True
TEMPLATE_DEBUG = DEBUG
SQL_DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

PRODUCT_ITEM_PER_PAGE = 8

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = "media/"

UPLOAD_DIR = MEDIA_ROOT + "upload/"
AVATAR_DIR = UPLOAD_DIR + "avatar/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    location('static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ueoiszm$cq$dwp%xja&amp;hs+w+@2!+e-0*ra++%6l+$4-u#rllqo'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    location(MEDIA_ROOT+'images/'),
    location('templates'),
    OSCAR_MAIN_TEMPLATE_DIR,
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
     'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',

    #Using Installed app
    'django.contrib.flatpages',
    'south',
    'compressor',
    'djcelery',
    'kombu.transport.django',
    'apps.common',

    #Override Oscar core
    'apps.catalogue', #you must run migrate in command, ex: python manage.py migrate catalogue
    'apps.partner',  #you must run migrate in command, ex: python manage.py migrate partner then read introduction in docs/Run_scheduled_task_with_celery.txt to run auto select price for products
    'apps.shipping',
    'apps.customer',

    #'redis_sessions_fork',
    'django_extensions',
    'sorl.thumbnail',
    'debug_toolbar',
    'haystack',
    'sorl.thumbnail',

    #New app
    'apps.watermark',#you must read introduction in docs/setting-site-for-bookmark-let-and-watermark.txt before
    'apps.collection',
    'rest_framework',
    'apps.bookmarklet',
    'apps.video',
    'apps.friendship',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

# Include core apps with a few overrides:
# - a shipping override app to provide some shipping methods
# - an order app to provide order processing logic
INSTALLED_APPS = INSTALLED_APPS + get_core_apps()

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'null': {
            'level': 'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'oscar.checkout': {
            'handlers': ['console'],
            'propagate': True,
            'level':'INFO',
        },
        'django.db.backends': {
            'handlers':['null'],
            'propagate': False,
            'level':'DEBUG',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    # Oscar specific
    'oscar.apps.search.context_processors.search_form',
    'oscar.apps.promotions.context_processors.promotions',
    'oscar.apps.checkout.context_processors.checkout',
    'oscar.apps.customer.notifications.context_processors.notifications',
    'oscar.core.context_processors.metadata',
    #Customize
    'context_processors.settings_values',
)

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.Emailbackend',
    'django.contrib.auth.backends.ModelBackend',
)
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

OSCAR_DEFAULT_CURRENCY = 'USD'
OSCAR_CURRENCY_LOCALE = 'en_US'

COUNTDOWN, LIST, SINGLE_PRODUCT, TABBED_BLOCK = (
    'Countdown', 'List', 'SingleProduct', 'TabbedBlock')
OSCAR_PROMOTION_MERCHANDISING_BLOCK_TYPES = (
    (COUNTDOWN, "Vertical list"),
    (LIST, "Horizontal list"),
    (TABBED_BLOCK, "Tabbed block"),
    (SINGLE_PRODUCT, "Single product"),
)

OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Processed', 'Cancelled',),
    'Cancelled': (),
}

#OSCAR_ACCOUNTS_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/accounts/'
APPEND_SLASH = True
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
OSCAR_ALLOW_ANON_CHECKOUT = True
OSCAR_SHOP_TAGLINE = 'eCommerce'
COMPRESS_ENABLED = False
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)


# Add Payflow dashboard stuff to settings

OSCAR_DASHBOARD_NAVIGATION.append(
    {
        'label': _('PayPal'),
        'icon': 'icon-globe',
        'children': [
            {
                'label': _('PayFlow transactions'),
                'url_name': 'paypal-payflow-list',
            },
            {
                'label': _('Express transactions'),
                'url_name': 'paypal-express-list',
            },
        ]
    })


BRAINTREE_MERCHANT = 'z3mss2xx8hpfjc39'
BRAINTREE_PUBLIC_KEY = 'fddpbjczc4qfjnq2'
BRAINTREE_PRIVATE_KEY = '9883af47d9ab5e54a21df8a0d7120da1'

##braintree config

Configuration.configure(
    Environment.Sandbox,
    BRAINTREE_MERCHANT,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)


# Taken from PayPal's documentation - these should always work in the sandbox
PAYPAL_SANDBOX_MODE = True
PAYPAL_API_VERSION = '88.0'
PAYPAL_ALLOW_NOTE = True


# These are the standard PayPal sandbox details from the docs - but I don't
# think you can get access to the merchant dashboard.
PAYPAL_API_USERNAME = '012kinglight-facilitator_api1.gmail.com'
PAYPAL_API_PASSWORD = '1382906590'
PAYPAL_API_SIGNATURE = 'A1k7ykd1YealrHS1QpIzp8QV4AeNA179j2LNcx3mfLqs9F5tEAjkExqt'

PAYPAL_PAYFLOW_VENDOR_ID = 'quantm'
PAYPAL_PAYFLOW_PASSWORD = '1324abdf'
PAYPAL_PAYFLOW_PARTNER = 'PayPal'

PAYPAL_PAYFLOW_CURRENCY = 'GBP'
PAYPAL_PAYFLOW_DASHBOARD_FORMS = True


#WATERMARK
FONT_PATH = PROJECT_ROOT + '/static/fonts/HelveticaNeueLTPro/HelveticaNeueLTPro-Hv.ttf'
WATERMARK_LOGO = STATIC_URL + 'images/uniweb_logo.png'
WATERMARK_LOGO_POSITION = (16, 16)
WATERMARK_TEXT = 'Using Signal'
WATERMARK_TEXT_COLOR = 255
WATERMARK_TEXT_FONT_SIZE = 16

#BOOKMARK LET
FORM_URL = '/bookmark-let/form'
STATIC_JS_URL = STATIC_URL + 'js/'
STATIC_CSS_URL = STATIC_URL + 'css/'
INIT_BOOKMARKLET_FILE = STATIC_JS_URL+ 'bookmarklet.js'
BOOKMARKLET_CSS_FILE = STATIC_CSS_URL + 'bookmarklet.css'
BOOKMARKLET_SAVE_FILE = STATIC_JS_URL + 'actions.js'
BOOKMARKLET_JS_AUTOCOMPLETE = STATIC_JS_URL + 'bootstrap-typeahead.js'


from datetime import timedelta
BROKER_URL = 'django://'
BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERYBEAT_PIDFILE = PROJECT_ROOT + "\celerybeat.pid"
CELERYBEAT_SCHEDULE = {
    'update-the-best-price-for-product': {
        'task': 'apps.partner.tasks.update_the_best_price_for_product',
        'schedule': timedelta(seconds=60)
    },
}
CELERY_ALWAYS_EAGER = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#redis sessions config
#SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_DB = 0
SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH = '/var/run/redis/redis.sock'
SESSION_REDIS_URL = 'redis://127.0.0.1:6379/0'

#VIDEO SETTINGS
VIDEO_THUMB = 'images/thumbs/'

#share_invite_type
CONFIG_SHARE = 1
CONFIG_INVITE = 2

EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_HOST_USER = 'tam@uniweb.vn'
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = '15aLAbXFdE8Yq7PTxLZExA'
EMAIL_PORT = 587

try:
    from integration import *
except ImportError:
    pass

try:
    from settings_local import *
except ImportError:
    pass
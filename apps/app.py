from oscar.app import Shop
from django.conf.urls import patterns, url, include
from oscar.core.loading import get_class
from oscar.core.application import Application
from .checkout.app import application as checkout_app
from .collection.app import application as collection_app
from .catalogue.app import application as catalogue_app
#from .dashboard.app import application as dashboard_app
from .promotions.app import application as promotions_app
from .basket.app import application as basket_app
from .customer.app import application as customer_app


class overriddenShop(Shop):
    # Specify a local checkout app where we override the payment details view
    checkout_app = checkout_app
    catalogue_app = catalogue_app
    #dashboard_app = dashboard_app
    promotions_app = promotions_app
    basket_app = basket_app
    customer_app = customer_app

shop = overriddenShop()


class url_shop(Application):

    def get_urls(self):
        urlpatterns = patterns('', (r'^', include(collection_app.urls)))
        return urlpatterns

application = url_shop()



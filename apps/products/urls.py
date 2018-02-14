#__author__ = 'tqn'
from django.conf.urls import *
from .views import MyProductView, ProductListAjaxView, MyProductListAjaxView


urlpatterns = patterns('apps.products.views',
   url(r'^ajax-product/', 'ajax_product'),
   url(r'^my-products/', MyProductView.as_view(), name='my-products'),
   url(r'^my-product/(?P<page>\d+)/', MyProductListAjaxView.as_view(), name='view-my-product-of-page'),
   url(r'^view-product-of-page/(?P<page>\d+)/', ProductListAjaxView.as_view(), name='view-product-of-page'),
)


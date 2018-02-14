#__author__ = 'tqn'
from django.conf.urls import *
from .views import *

urlpatterns = patterns('apps.collection.views',
   #Using in collection design
   url(r'^open/$', CollectionListView.as_view(), name='collection_open'),
   url(r'^list/$', ViewCollection.as_view(), name='collection_list_item'),
   url(r'^save/$', 'collection_save', name='collection_save'),
   url(r'^item/(?P<set_id>\d+)/$', 'collection_open_item', name='collection_open_item'),

   #Add product to Collection in front-end
   url(r'add-product-to-collection-form/$', MyCollectionForm.as_view(), name='add_product_to_collection_form'),
   url(r'add-product-to-collection/$', 'add_product_to_collection', name='add_product_to_collection'),
   url(r'preview/(?P<collection_id>\d+)/$', MyCollectionPreview.as_view(), name='preview_collection_before_go_design_page'),
   url(r'^gallery-save/$', 'gallery_save_into_collection', name='gallery_save_into_collection'),

   #Share
   url(r'^share/$', 'save_share_collection', name='save_share_collection'),
   url(r'^invite/$', 'save_invite_edit_collection', name='save_invite_edit_collection'),
   url(r'^update_edit/$', 'update_edit', name='update_edit'),
   url(r'^save_comment/$', 'save_comment', name='save_comment'),
   url(r'my-collections', MyCollectionView.as_view(), name='my-collections'),

   #My list
   url(r'^my-list/$', MyListProfile.as_view(), name='my-list-profile'),
   url(r'^my-list/(?P<pk>\d+)/$', MyListDetail.as_view(), name='my-list-detail'),
   url(r'^my-list/(?P<pk>\d+)/delete/$', MyListDelete.as_view(), name='my-list-delete'),
   url(r'^my-list/remove/(?P<list_pk>\d+)/(?P<item_id>\d+)/$', 'my_list_remove_item', name='my-list-remove'),

   #Comment
   url(r'^collection/delete/$', 'delete_comment', name='delete_comment'),
)




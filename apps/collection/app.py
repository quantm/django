from django.conf.urls import patterns, url
from oscar.core.application import Application
from apps.collection import views


class CollectionApplication(Application):
    name = 'collection'
    collection_index = views.ProductListCollection
    category_index = views.CategoryListView
    search_views = views.Search
    comment_views = views.ViewCollectionComment

    def get_urls(self):
        urlpatterns = patterns('',
                               url(r'^product/$', self.collection_index.as_view(), name='collection_index'),
                               url(r'^category/$', self.category_index.as_view(), name='category_index'),
                               url(r'^search/$', self.search_views.as_view(), name='product_search'),
                               url(r'^comment/$', self.comment_views.as_view(), name='collection_list_comment'),
                               )
        return self.post_process_urls(urlpatterns)


application = CollectionApplication()





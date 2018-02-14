from oscar.apps.catalogue.views import ProductListView as CoreProductListView
from django.db.models import get_model
import settings

Product = get_model('catalogue', 'product')

class ProductListView(CoreProductListView):
    paginate_by = settings.PRODUCT_ITEM_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        q = self.get_search_query()
        qs = Product.browsable.base_queryset()
        if q:
            # Send signal to record the view of this product
            self.search_signal.send(sender=self, query=q, user=self.request.user)
            return qs.filter(title__icontains=q)
        else:
            return qs.filter(stockrecords__isnull=False).distinct()
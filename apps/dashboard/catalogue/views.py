# Create your views here.
from django.utils.translation import ugettext_lazy as _

from oscar.apps.catalogue.models import Product
from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView as CoreProductCreateUpdateView, ProductListView as CoreProductListView
from oscar.apps.dashboard.catalogue.forms import ProductForm, ProductCategoryFormSet, ProductImageFormSet, ProductRecommendationFormSet
from .forms import StockRecordFormSet


class ProductCreateUpdateView(CoreProductCreateUpdateView):
    template_name = 'dashboard/catalogue/product_update.html'
    model = Product
    context_object_name = 'product'
    form_class = ProductForm
    category_formset = ProductCategoryFormSet
    image_formset = ProductImageFormSet
    recommendations_formset = ProductRecommendationFormSet
    stockrecord_formset = StockRecordFormSet

    def get_context_data(self, **kwargs):
        ctx = super(ProductCreateUpdateView, self).get_context_data(**kwargs)
        ctx['stockrecord_formset'] = self.stockrecord_formset(self.product_class, request=self.request, instance=self.object)
        ctx['number_stock'] = None
        if self.request.user.is_superuser:
            ctx['number_stock'] = 2

        return ctx

class ProductListView(CoreProductListView):

    def get_queryset(self):
        """
        Build the queryset for this list and also update the title that
        describes the queryset
        """
        description_ctx = {'upc_filter': '',
                           'title_filter': ''}
        queryset = self.model.objects.base_queryset().select_related(
            'stockrecord__partner').order_by('-date_created')
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            self.description = self.description_template % description_ctx
            return queryset

        data = self.form.cleaned_data

        if data['upc']:
            queryset = queryset.filter(upc=data['upc'])
            description_ctx['upc_filter'] = _(" including an item with UPC '%s'") % data['upc']

        if data['title']:
            queryset = queryset.filter(title__icontains=data['title']).distinct()
            description_ctx['title_filter'] = _(" including an item with title matching '%s'") % data['title']

        self.description = self.description_template % description_ctx

        return queryset
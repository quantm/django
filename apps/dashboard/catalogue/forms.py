__author__ = 'tqn'
from django import forms
from django.db.models import get_model
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from oscar.apps.dashboard.catalogue.forms import ProductForm as CoreProductForm, BaseStockRecordFormSet, StockRecordForm
from apps.partner.models import StockRecord, Partner


Product = get_model('catalogue', 'Product')
BaseStockRecordFormSet = inlineformset_factory(Product, StockRecord, form=StockRecordForm, extra=1)

class StockRecordFormSet(BaseStockRecordFormSet):

    def __init__(self, product_class, *args, **kwargs):
        self.product_class = product_class
        if 'request' in kwargs:
            self.request = kwargs['request']
            del kwargs['request']
        super(StockRecordFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['product_class'] = self.product_class
        stock_record_form = super(StockRecordFormSet, self)._construct_form(i, **kwargs)
        if hasattr(self, 'request'):
            user = self.request.user
            if user.is_staff and user.is_superuser:
                for field in stock_record_form.fields:
                    stock_record_form.fields[field].widget = forms.widgets.HiddenInput()
                    st = 1
                #pass
            else:
                partner = Partner.objects.filter(users=user.id)
                if list(partner).__len__() > 0:
                    stock_record_form.fields['partner'].queryset = partner
                    stock_record_form.fields['partner'].widget = forms.widgets.HiddenInput()
                    stock_record_form.fields['partner'].initial = list(partner)[0].pk

            stock_record_form.fields['selected_partner'].widget = forms.widgets.HiddenInput()
            stock_record_form.fields['selected_partner'].initial = 0

            partner_value_id = stock_record_form.instance.partner_id
            stock_record_form.fields['partner'].queryset = Partner.objects.filter(id=partner_value_id)
            stock_record_form.fields['partner'].widget = forms.widgets.HiddenInput()

        return stock_record_form

    def get_queryset(self):

        if not hasattr(self, 'request'):
            self.extra = 0
            return super(StockRecordFormSet, self).get_queryset().order_by('-selected_partner','price_excl_tax')
        else:
            user = self.request.user
            if(user.is_staff and user.is_superuser):
                #Don't allow admin add more stock price
                self.extra = 0

                return super(StockRecordFormSet, self).get_queryset().order_by('-selected_partner','price_excl_tax')
            else:
                partner = Partner.objects.filter(users=user)
                qs = StockRecord.objects.filter(product=self.instance, partner=partner).exclude(selected_partner=1)
                #limit stock record form show with current partner
                if list(qs).__len__() > 0:
                    #If current partner already input price, don't allow partner add more price
                    self.extra = 0
                else:
                    #If current not yet input price, show 1 stock record form
                    self.extra = 1

                return qs
class ProductForm(CoreProductForm):
    pass
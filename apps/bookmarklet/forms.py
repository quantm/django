#__author__ = 'tqn'
from django import forms
from oscar.apps.catalogue.models import Product, ProductClass, ProductImage
PRODUCT_OPTIONS = (
    ('0', u'A new Product'),
    ('1', u'To trending'),
)
VIDEO_OPTIONS = (
    ('0', u'To My Videos'),
    ('1', u'To trending'),
)


class BookmarkLetForm(forms.Form):
    title = forms.CharField(error_messages={'required': 'Please enter title'})
    description = forms.CharField(widget=forms.Textarea, label='Description', required=False)
    image = forms.CharField(widget=forms.HiddenInput)
    product_is_trending = forms.ChoiceField(choices=PRODUCT_OPTIONS)
    video_code = forms.CharField(widget=forms.HiddenInput)
    video_is_trending = forms.ChoiceField(choices=VIDEO_OPTIONS)

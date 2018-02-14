#__author__ = 'tqn'
from django import forms
from oscar.apps.catalogue.models import Product, ProductClass, ProductImage

VIDEO_OPTIONS = (
    ('0', u'To My Videos'),
    ('1', u'To trending'),
)

class VideoForm(forms.Form):
    title = forms.CharField(error_messages={'required': 'Please enter title'})
    description = forms.CharField(widget=forms.Textarea, label='Description', required=False)
    image = forms.CharField(widget=forms.HiddenInput)
    video_code = forms.CharField(widget=forms.HiddenInput)
    video_is_trending = forms.ChoiceField(choices=VIDEO_OPTIONS)
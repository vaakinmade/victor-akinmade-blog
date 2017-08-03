from django import forms
from django.core.urlresolvers import reverse


class SearchForm(forms.Form):
    searchbox = forms.CharField(widget=forms.TextInput())

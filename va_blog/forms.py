from django import forms
from django.core import validators


class SuggestionForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}))
    suggestion = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40, 'placeholder':'Question or Suggestion'}))

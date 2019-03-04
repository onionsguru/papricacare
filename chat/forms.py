from django import forms
from django.forms import widgets
from chat import models

class EnterForm(forms.Form):
    input_text = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'id':'input_text', 'autofocus':'autofocus', 'autocomplete':'off'}))

    def get_data(self):
        if self.is_valid():
            return self.cleaned_data
        return
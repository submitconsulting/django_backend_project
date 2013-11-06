from django import forms
from django.forms import ModelForm

#no usado, eliminar
class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
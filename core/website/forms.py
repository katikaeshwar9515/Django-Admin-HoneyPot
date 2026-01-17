from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    file = forms.ImageField(widget=forms.ClearableFileInput())
    class Meta:
        model = Photo
        fields = ('file', )
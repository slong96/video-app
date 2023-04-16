from django import forms 
from .models import Video

# this is the form field to display in add.html
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name', 'url', 'notes'] # this needs to match the ones in model.py


class SearchForm(forms.Form):
    search_term = forms.CharField()
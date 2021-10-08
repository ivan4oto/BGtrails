from django import forms
from django.forms import widgets

from .models import Trail


class TrailForm(forms.ModelForm):
    class Meta:
        model = Trail
        fields = [
            'name',
            'description',
            'gpx_file',
            'tag'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'description': forms.Textarea(attrs={'class': "form-control"}),
            'gpx_file': forms.FileInput(attrs={'class': 'form-control'}),
            'tag': forms.Select(attrs={'class': 'form-select'}),

        }

class TrailUpdateForm(forms.ModelForm):
    class Meta:
        model = Trail
        fields = [
            'name',
            'distance',
            'elevation',
            'description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control", "id":"trail-name"}),
            'distance': forms.NumberInput(attrs={'class': "form-control", 'id': 'trail-distance'}),
            'elevation': forms.NumberInput(attrs={'class': "form-control", 'id': 'trail-elevation'}),
            'description': forms.Textarea(attrs={'class': "form-control", 'id': 'trail-description'})
        }
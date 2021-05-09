from django import forms

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
            'description',
            'gpx_file',
            'tag'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'distance': forms.NumberInput(attrs={'class': 'form-control'}),
            'elevation': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': "form-control"}),
            'gpx_file': forms.FileInput(attrs={'class': 'form-control'}),
            'tag': forms.Select(attrs={'class': 'form-select'}),

        }
from django import forms

from .models import Trail


class TrailForm(forms.ModelForm):
    class Meta:
        model = Trail
        fields = [
            'name',
            'description',
            'gpx_file'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'textarea'}),
            'gpx_file': forms.FileInput(attrs={'class': 'file-input'})
        }
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
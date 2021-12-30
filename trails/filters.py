import django_filters
from django import forms

from .models import Trail


class TrailFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': "Search..."
        }))

    distance_lt = django_filters.NumberFilter(field_name='distance', lookup_expr='lt', widget=forms.NumberInput(attrs={'class': "form-control"}))
    distance_gt = django_filters.NumberFilter(field_name='distance', lookup_expr='gt', widget=forms.NumberInput(attrs={'class': "form-control"}))

    elevation_lt = django_filters.NumberFilter(field_name='elevation', lookup_expr='lt', widget=forms.NumberInput(attrs={'class': "form-control"}))
    elevation_gt = django_filters.NumberFilter(field_name='elevation', lookup_expr='gt', widget=forms.NumberInput(attrs={'class': "form-control"}))

    class Meta: 
        model = Trail
        fields = ('name', 'distance', 'elevation')

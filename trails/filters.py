import django_filters

from .models import Trail


class TrailFilter(django_filters.FilterSet):
    class Meta: 
        model = Trail
        fields = {
            'name': ['exact'],
            'distance': ['lt', 'gt'],
            'elevation': ['lt', 'gt']
        }

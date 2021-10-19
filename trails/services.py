from django.core.exceptions import ValidationError
from django.core.files import File
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from geojson_transformer import GeoJsonTransformer
# from io import StringIO 
import os

from .models import Trail


User = get_user_model()

# Trail Model Service

class TrailServiceHelper():
    
    def create_trail(self, *, name: str, description: str, distance: float, elevation: int, gpx_file: File, user: User, tag: str) -> Trail:
        if gpx_file is None:
            raise ValidationError('Trail objects must have a gpx file.')

        transformer = GeoJsonTransformer(in_memory_file=gpx_file)
        trail_object = Trail(
            name=name,
            description=description,
            distance=distance if distance else transformer.total_distance,
            elevation=elevation if elevation else transformer.total_elevation,
            location=Point(transformer.starting_point[0], transformer.starting_point[1]),
            gpx_file=gpx_file,
            csv_file=extract_csv_file(transformer=transformer),
            user=user,
            tag=tag
        )
        trail_object.full_clean()
        trail_object.save()

        return trail_object

    def update_trail(self, *, form: dict, pk: int, gpx_file=None) -> Trail:
        trail_object = Trail.objects.get(pk=pk)
        for attr, val in form.items():
            if val is not None:
                setattr(trail_object, attr, val)
        trail_object.save()

        return trail_object

# Transformer Service

def extract_distance(*, gpx_file=File) -> float:
    distance = GeoJsonTransformer(in_memory_file=gpx_file).total_distance
    return distance

def extract_elevation(*, gpx_file=File) -> int:
    elevation = GeoJsonTransformer(in_memory_file=gpx_file).total_elevation
    return elevation

def extract_starting_point(*, gpx_file=File) -> Point:
    transformer = GeoJsonTransformer(in_memory_file=gpx_file)
    starting_point = Point(transformer.starting_point[0], transformer.starting_point[1])
    return starting_point

def extract_csv_file(*, transformer=GeoJsonTransformer) -> File:   
    transformer.to_csv()
    csv_name = transformer.name + '.' + 'csv'
    f = open(csv_name, 'rb')
    prepared_file = File(f)
    csv_uploaded_file = InMemoryUploadedFile(f, '', csv_name, 'text/csv', prepared_file.size, None)
    os.remove(csv_name)

    return csv_uploaded_file
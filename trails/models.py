from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.conf import settings
from django.core.files import storage
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File
from django.forms.widgets import Media
from geojson_transformer import GeoJsonTransformer
from .storages import MediaStorage
from .validators import FileValidator
from .services import get_starting_point, get_total_distance, get_total_elevation


User = settings.AUTH_USER_MODEL
validate_file = FileValidator(max_size=2048 * 1000,
                              content_types=('text/xml',))
fs = FileSystemStorage(location='cdn_test/media')

# Create your models here.
class Trail(models.Model):
    TAG_CHOICES = [
        ('KE', 'Ком Емине'),
        ('RL', 'Рила'),
        ('VS', 'Витоша'),
        ('SP', 'Стара Планина'),
        ('PN', 'Пирин'),
        ('RP', 'Родопи'),
        ('ZB', 'Западен Балкан'),
        ('CB', 'Централен Балкан'),
        ('IB', 'Източен Балкан')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    distance = models.FloatField(null=True, blank=True)
    elevation = models.IntegerField(null=True, blank=True)
    location = models.PointField(null=True, blank=True)
    gpx_file = models.FileField(storage=MediaStorage, upload_to='trails/gpx', null=True, blank=True,
                                validators=[validate_file])
    csv_file = models.FileField(storage=MediaStorage, upload_to='trails/csv', null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tag = models.CharField(max_length=25, choices=TAG_CHOICES, null=True)


    def save(self, *args, **kwargs):
        self.full_clean()
        self._set_properties()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse(viewname='detail-trail', args=[str(self.id)])

    def _set_location(self):
        coordinates = get_starting_point(self.gpx_file.file)
        pnt = Point(coordinates[0], coordinates[1])
        print(coordinates[0], coordinates[1])
        self.location = pnt
    
    def _set_elevation(self):
        self.elevation = get_total_elevation(self.gpx_file.file)

    def _set_distance(self):
        self.distance = get_total_distance(self.gpx_file.file)

    def _set_properties(self):
        geojson_model = GeoJsonTransformer(in_memory_file=self.gpx_file)
        self.location = Point(geojson_model.starting_point[0], geojson_model.starting_point[1])
        self.elevation = geojson_model.total_elevation
        self.distance = geojson_model.total_distance
        geojson_model.to_csv()
        self._build_csv(geojson_model)

        
        # self._set_location()
        # self.gpx_file.seek(0) #TODO: look for different solution to thet seek() method
        # self._set_elevation()
        # self.gpx_file.seek(0)
        # self._set_distance()
        # self.gpx_file.seek(0)
        
    def _build_csv(self, geojson_model):
        geojson_model.to_csv()
        csv_name = geojson_model.name + '.' + 'csv'
        f = open(csv_name, 'rb')
        prepared_file = File(f)
        self.csv_file = InMemoryUploadedFile(f, '', csv_name, 'text/csv', prepared_file.size, None)

    def get_lat(self):
        return self.location.x

    def get_lon(self):
        return self.location.y

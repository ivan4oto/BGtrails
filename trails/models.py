from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.conf import settings

from .storages import MediaStorage
from .validators import FileValidator
from .services import get_starting_point, get_total_distance, get_total_elevation

User = settings.AUTH_USER_MODEL
validate_file = FileValidator(max_size=2048 * 1000, 
                             content_types=('text/xml',))

# Create your models here.
class Trail(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    distance = models.FloatField(null=True, blank=True)
    elevation = models.IntegerField(null=True, blank=True)
    location = models.PointField(null=True, blank=True)
    gpx_file = models.FileField(storage=MediaStorage, upload_to='trails', null=True, blank=True,
                                validators=[validate_file])
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # tag = models.CharField(max_length=25, null=True)


    def save(self, *args, **kwargs):
        self.full_clean()
        self._set_properties()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse(viewname='detail-trail', args=[str(self.id)])

    def _set_location(self):
        coordinates = get_starting_point(self.gpx_file.file)
        pnt = Point(coordinates[1], coordinates[0])
        self.location = pnt
    
    def _set_elevation(self):
        self.elevation = get_total_elevation(self.gpx_file.file)

    def _set_distance(self):
        self.distance = get_total_distance(self.gpx_file.file)

    def _set_properties(self):
        self._set_location()
        self.gpx_file.seek(0)
        self._set_elevation()
        self.gpx_file.seek(0)
        self._set_distance()
        self.gpx_file.seek(0)

    def get_lat(self):
        return self.location.x

    def get_lon(self):
        return self.location.y
    
    # def _to_geojson(self):
    #     geojson_file = 
    #     self.gpx_file.file = 
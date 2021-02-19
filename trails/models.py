from django.contrib.gis.db import models
from django.conf import settings

from .validators import validate_is_gpx

# Create your models here.
class Trail(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    distance = models.FloatField(null=True)
    elevation = models.FloatField(null=True)
    location = models.PointField(null=True)
    gpx_file = models.FileField(storage=ProtectedStorage, upload_to='products/', null=True, blank=True,
                                validators=(validate_is_gpx,))
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


    def set_location(self):
        #.
        return False
    
    def set_elevation(self)
        #.
        return False
    
    def set_distance(self):
        #.
        return False

    def get_filename(self):
        #.
        return False
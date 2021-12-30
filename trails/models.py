from django.conf import settings
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from .storages import MediaStorage
from .validators import FileValidator


User = settings.AUTH_USER_MODEL
validate_file = FileValidator(max_size=2048 * 1000,
                              content_types=('text/xml',))
fs = FileSystemStorage(location='cdn_test/media')

# Create your models here.
class Trail(models.Model):
    TAG_CHOICES = [
        ('KE', 'Ком Емине'),
        ('RC', 'Състезание'),
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
    static_map = models.ImageField(storage=MediaStorage, upload_to='images/', null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tag = models.CharField(max_length=25, choices=TAG_CHOICES, null=True)

    def delete(self, using=None, keep_parents=False):
        self.gpx_file.storage.delete(self.gpx_file.name)
        self.csv_file.storage.delete(self.csv_file.name)
        super().delete()

    def clean(self):
        if self.gpx_file is None:
            raise ValidationError('Trail objects must have a gpx file.')
        if self.csv_file is None:
            raise ValidationError('Trail objects must have a csv file.')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse(viewname='detail-trail', args=[str(self.id)])

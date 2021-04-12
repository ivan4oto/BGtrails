from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from storages.backends.s3boto3 import S3Boto3Storage


BUCKET_NAME = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
if BUCKET_NAME == None:
    raise ImproperlyConfigured("BUCKET_NAME is not set in settings.py")

# django-storages
class MediaStorage(S3Boto3Storage):
    bucket_name = BUCKET_NAME
    location = 'media'

class StaticStorage(S3Boto3Storage):
    bucket_name = BUCKET_NAME
    location = ''
    # location = 'trails'
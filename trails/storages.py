from django.conf import settings
import os
from django.core.exceptions import ImproperlyConfigured
from django.forms.widgets import Media
from storages.backends.s3boto3 import S3Boto3Storage, SpooledTemporaryFile


BUCKET_NAME = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
if BUCKET_NAME is None:
    raise ImproperlyConfigured("BUCKET_NAME is not set in settings.py")


# django-storages
class MediaStorage(S3Boto3Storage):
    bucket_name = BUCKET_NAME
    location = 'media'

    # def _save(self, name, content):
    #     content.seek(0, os.SEEK_SET)
    #     with SpooledTemporaryFile() as content_autoclose:
    #         content_autoclose.write(content.read())
    #         return super(MediaStorage, self)._save(name, content_autoclose)

    # def _save_content(self, obj, content, parameters):
    #     """
    #     We create a clone of the content file as when this is passed to boto3 it wrongly closes
    #     the file upon upload where as the storage backend expects it to still be open
    #     """
    #     content.seek(0, os.SEEK_SET)
    #     content_autoclose = SpooledTemporaryFile()
    #     content_autoclose.write(content.read())
    #     super(MediaStorage, self)._save_content(obj, content_autoclose, parameters)
        
    #     if not content_autoclose.closed:
    #         content_autoclose.close()


class StaticStorage(S3Boto3Storage):
    bucket_name = BUCKET_NAME
    location = ''
    # location = 'trails'

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ImproperlyConfigured


MEDIA = getattr(settings, 'MEDIA_ROOT', None)
if MEDIA == None:
    raise ImproperlyConfigured("MEDIA_ROOT is not set in settings.py")

# django-storages
class MediaStorage(FileSystemStorage):
    location = MEDIA
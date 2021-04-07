from django.db import models
from trails.models import Trail
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    favourites = models.ManyToManyField(Trail, related_name='favorited_by')
    

from django.contrib.auth.models import User
from django.contrib.auth.models import User, Group
from django.db import models
from django.utils import timezone
from django_measurement.models import MeasurementField
from measurement.measures import Distance
from django.urls import reverse
from coordinates import get_distance


class Adventurer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=64)
    distance = MeasurementField(measurement=Distance)
    elevation = MeasurementField(measurement=Distance)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    want_go = models.ManyToManyField(Adventurer, related_name='want_go_adventurer_set')
    been_there = models.ManyToManyField(Adventurer, related_name='been_there_adventurer_set')
    author = models.ForeignKey(Adventurer, null=True, on_delete=models.SET_NULL, related_name='Adventurer')
    file = models.FileField()
    image = models.ImageField(blank=True)

    def in_range(self, coords, range_km):
        r = get_distance((self.lat, self.lon, ), (float(coords[0]), float(coords[1])))
        return r <= float(range_km)

    def get_absolute_url(self):
        return reverse("detail", kwargs={'post_id': self.id})

    def __str__(self):
        return f'Title: {self.title}, Distance: {self.distance}'


class PostImage(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.post.title


CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
]


class Rate(models.Model):
    is_visited = models.BooleanField(default=False, null=True)
    rate = models.IntegerField(choices=CHOICES, null=True)
    comments = models.TextField(null=True)
    author = models.ForeignKey(Adventurer, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.rate

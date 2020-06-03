from django import forms
from django.contrib.auth.models import User, Group
from django.db import models
from django.utils import timezone
from django_measurement.models import MeasurementField
from measurement.measures import Distance


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
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Adventurer, null=True, on_delete=models.SET_NULL)
    file = models.FileField(null=True)

    def __str__(self):
        return f'Title: {self.title}, Distance: {self.distance}'

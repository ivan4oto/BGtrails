from django.db import models

from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django_measurement.models import MeasurementField
from measurement.measures import Distance


class Post(models.Model):
    title = models.CharField(max_length=64)
    distance = MeasurementField(measurement=Distance)
    elevation = MeasurementField(measurement=Distance)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    file = forms.FileField()

    def __str__(self):
        return f'Title: {self.title}, Distance: {self.distance}'

from django.db import models
from django.contrib.auth.models import User

class Venue(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location_latitude = models.FloatField()
    location_longitude = models.FloatField()

    def __str__(self):
        return self.name

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    datetime = models.CharField(max_length=100)  # Can change to DateTimeField if preferred
    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_image = models.CharField(max_length=255)  # Can also use ImageField if storing images

    def __str__(self):
        return self.name

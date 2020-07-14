from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

class Location(models.Model):
    
    name = models.CharField(max_length=255)
    country = models.TextField()
    lat = models.TextField()
    lon = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('location_detail', args=[str(self.id)])

class Author(models.Model):
    
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author_detail', args=[str(self.id)])


class Project(models.Model):
    name = models.CharField(max_length=255)
    details = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    electricity = models.BooleanField(default=False)
    heat = models.BooleanField(default=False)
    gas = models.BooleanField(default=False)
    h2 = models.BooleanField(default=False)
    ev = models.BooleanField(default=False)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='location',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='location',
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.id)])
        

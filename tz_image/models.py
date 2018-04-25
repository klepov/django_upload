from django.db import models

# Create your models here.
from tz_profile.models import Profile


class Image(models.Model):
    original = models.ImageField(upload_to='images')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    link = models.CharField(max_length=255,blank=True)


class Resolution(models.Model):
    link = models.CharField(max_length=255)
    original = models.ForeignKey(Image, on_delete=models.CASCADE)
    format_required = models.CharField(max_length=255, blank=True)

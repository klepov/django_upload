from django.contrib import admin

# Register your models here.
from tz_image.models import Resolution, Image

admin.site.register(Resolution)
admin.site.register(Image)

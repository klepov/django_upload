from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from rest_framework.authtoken.models import Token


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        Token.objects.get_or_create(user=self.user)
        super().save(force_insert, force_update, using, update_fields)


# Generated by Django 2.0 on 2018-04-25 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tz_image', '0003_resolution_format_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='link',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]

# Generated by Django 2.0 on 2018-04-24 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tz_image', '0002_auto_20180424_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='resolution',
            name='format_required',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]

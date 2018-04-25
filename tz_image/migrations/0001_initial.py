# Generated by Django 2.0 on 2018-04-23 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tz_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.ImageField(upload_to='images')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tz_profile.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Resolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.PositiveIntegerField()),
                ('width', models.PositiveIntegerField()),
                ('link', models.CharField(max_length=255)),
                ('original', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tz_image.Image')),
            ],
        ),
    ]

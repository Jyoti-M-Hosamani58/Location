# Generated by Django 5.0.6 on 2024-11-07 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='location_sharing_active',
            field=models.BooleanField(default=False),
        ),
    ]

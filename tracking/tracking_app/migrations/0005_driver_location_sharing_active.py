# Generated by Django 5.0.6 on 2024-11-10 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking_app', '0004_remove_driver_location_sharing_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='location_sharing_active',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

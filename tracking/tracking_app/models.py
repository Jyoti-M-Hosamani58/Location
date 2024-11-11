from django.db import models

# Create your models here.
class Driver(models.Model):
    phonenumber = models.CharField(max_length=15, unique=True,null=True)
    name = models.CharField(max_length=100,null=True)
    location_sharing_active = models.CharField(max_length=100,null=True)
    # Add any other driver-related fields

    def __str__(self):
        return self.name

class DriverLocation(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='locations',null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now=True,null=True)
    location_sharing_active = models.BooleanField(default=False,null=True)

    def __str__(self):
        return f"Location for {self.driver.name} at {self.timestamp}"
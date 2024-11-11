from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import json
from .models import Driver, DriverLocation
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


# Check if location sharing is active
@csrf_exempt
def check_location_sharing_status(request):
    phone_number = request.GET.get('phone_number')

    if not phone_number:
        return JsonResponse({"status": "error", "message": "Phone number is required."})

    try:
        location = DriverLocation.objects.get(driver__phonenumber=phone_number)

        # Check if location sharing is active. If not, activate it.
        if not location.location_sharing_active:
            location.location_sharing_active = True
            location.save()

        return JsonResponse({
            "location_sharing_active": location.location_sharing_active
        })
    except DriverLocation.DoesNotExist:
        # If the location doesn't exist, create a new record with location_sharing_active set to True
        driver = Driver.objects.get(phonenumber=phone_number)  # Find the driver by phone number
        location = DriverLocation.objects.create(
            driver=driver,
            latitude=0.0,  # Default location (you can set to a real default value)
            longitude=0.0,
            timestamp=datetime.now(),
            location_sharing_active=True  # Activate location sharing by default when creating
        )
        return JsonResponse({"location_sharing_active": True})

import json
from django.http import JsonResponse
from datetime import datetime

@csrf_exempt
def update_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data.get("phone_number")
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            timestamp = data.get("timestamp")

            # Debugging: Print the data being received from the frontend
            print(f"Received data: {data}")

            # Check if required data is missing
            if not phone_number or not latitude or not longitude or not timestamp:
                return JsonResponse({"status": "error", "message": "Missing required fields."})

            # Validate the latitude and longitude values
            if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
                return JsonResponse({"status": "error", "message": "Invalid latitude or longitude format."})

            if latitude == 0 or longitude == 0:
                return JsonResponse({"status": "error", "message": "Invalid location (latitude or longitude cannot be zero)."})

            # Check if the driver exists
            try:
                driver = Driver.objects.get(phonenumber=phone_number)
            except Driver.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Driver not found."})

            # Save or update the driver's location in the DriverLocation table
            location, created = DriverLocation.objects.update_or_create(
                driver=driver,
                defaults={
                    "latitude": latitude,
                    "longitude": longitude,
                    "timestamp": timestamp,
                    "location_sharing_active": True,  # Ensure sharing is active
                }
            )

            return JsonResponse({"status": "success", "message": "Location updated successfully."})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format."})

    return JsonResponse({"status": "error", "message": "Invalid request method."})


@csrf_exempt
def stop_location(request, phone_number):
    if request.method == "POST":
        try:
            driver = Driver.objects.get(phonenumber=phone_number)
            # Deactivate location sharing
            location = DriverLocation.objects.filter(driver=driver).order_by('-timestamp').first()
            if location:
                location.location_sharing_active = False
                location.save()
            return JsonResponse({'status': 'Location sharing stopped'})
        except Driver.DoesNotExist:
            return JsonResponse({'status': 'Driver not found'}, status=404)
    return JsonResponse({'status': 'Method not allowed'}, status=405)

def location(request):
    return render(request,'update_location.html')

def track_driver(request, phone_number):
    # Fetch the driver by phone number
    driver = get_object_or_404(Driver, phonenumber=phone_number)

    # Try to get the latest location or return None if no location exists
    location = DriverLocation.objects.filter(driver=driver).order_by('-timestamp').first()

    # Pass the driver and location to the template
    return render(request, 'track_driver.html', {
        'driver': driver,
        'location': location,
    })
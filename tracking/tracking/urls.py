"""
URL configuration for tracking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tracking_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.location,name='location'),
    # URL for updating the driver's location
    path('check_location_sharing_status/', views.check_location_sharing_status),
    path('update_location/', views.update_location),
    path('stop_location/<str:phone_number>/', views.stop_location),
    path('track_driver/<str:phone_number>/', views.track_driver, name='track_driver'),

]

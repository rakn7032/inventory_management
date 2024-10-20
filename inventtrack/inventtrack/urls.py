from django.contrib import admin
from django.urls import path, include

"""
Defines the URL routing configuration for the inventtrack project.

The `urlpatterns` list routes URLs to views for different modules:
1. The 'admin/' URL is routed to Django's default admin interface.
2. The 'auth/' URL is routed to the `authentication` app's URLs, managing user authentication-related operations.
3. The 'inventory/' URL is routed to the `inventory` app's URLs, handling inventory management functionalities.
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('authentication.urls')),
    path('inventory/',include('inventory.urls')),
]

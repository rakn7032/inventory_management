"""
URL configuration for inventtrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

"""emr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static

from patients.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('', include('accounts.urls')),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('location/', include('locations.urls')),
    path('visits/', include('visits.urls')),
    path('vitals/', include('vitals.urls')),
    path('medical_services/', include('medical_services.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('radiology/', include('radiology.urls')),
    path('bills/', include('bills.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
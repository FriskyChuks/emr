
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from patients.views import home

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('home/', home, name='home'),
    path('', include('accounts.urls')),
    path('accounts/', include('accounts.password.urls')),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('location/', include('locations.urls')),
    path('visits/', include('visits.urls')),
    path('vitals/', include('vitals.urls')),
    path('medical_services/', include('medical_services.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('radiology/', include('radiology.urls')),
    path('bills/', include('bills.urls')),
    path('labs/', include('labs.urls')),
    path('diagnosis/', include('diagnosis.urls')),
    path('reports/', include('reports.urls')),
    # path('chaining/', include('smart_selects.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

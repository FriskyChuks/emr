from django import urls
from django.urls import path

from .views import clinic_view, ward_view

urlpatterns = [
    path('clinic/', clinic_view, name='clinic_view'),
    path('ward/', ward_view, name='ward_view'),    
]
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import create_medical_service_view, raise_patient_medical_service_view, search_medical_service_view

urlpatterns = [
    path("create_medical_service/", create_medical_service_view, name="create_medical_service"),
    path("raise_patient_medical_service/<encounter_id>/", raise_patient_medical_service_view, name="raise_patient_medical_service"),
    path("search_service/", csrf_exempt(search_medical_service_view), name="search_service_view"),
]
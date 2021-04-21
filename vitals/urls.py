from django.urls import path

from .views import take_vital_signs_view, patient_notes_view


urlpatterns = [
    path("take_vital_signs/<id>", take_vital_signs_view, name="take_vital_signs"),
    path("add_notes/<id>", patient_notes_view, name="patient_notes"),
]
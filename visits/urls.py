from django.urls import path

from .views import(
    clinic_visits_display_view, 
    create_new_encounter, 
    discharge_patient_view, 
    transfer_patient_view, 
    ward_visits_display_view
    # create_patient_bills_view
)

urlpatterns = [
    path("clinic_visits_display/<id>", clinic_visits_display_view, name='clinic_visits_display'),
    path("ward_admission_display/<id>", ward_visits_display_view, name='ward_admission_display'),
    path("create_encounter/<patient_id>/", create_new_encounter, name='create_new_encounter'),
    path("discharge_patient/<id>/", discharge_patient_view, name='discharge_patient'),
    path("transfer_patient_view/<id>/", transfer_patient_view, name='transfer_patient'),
]


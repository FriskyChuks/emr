from django.urls import path

from django import forms

from .forms import PatientBiodataForm
from .preview import PatientBiodataFormPreview

from .views import(
    patient_registration_form, 
    patient_detail_view, 
    search_patient_view,
    patient_folder_view,
    patient_archives_view,
    upload_patient_image_form
    #upload_foto,
)  

urlpatterns = [
    path('registration/', patient_registration_form, name='registration'),
    path('search/', search_patient_view, name='search_patient'),
    path('patient_info/<id>/', patient_detail_view, name='patient_detail'),
    path('patient_folder/<enc_id>/', patient_folder_view, name='patient_folder'),
    path('patient_archives/<patient_id>/', patient_archives_view, name='archives'),
    path('upload_image/<pid>/', upload_patient_image_form, name='upload_image'),
    path('patient_registration/', PatientBiodataFormPreview(PatientBiodataForm), name="reg"),
]
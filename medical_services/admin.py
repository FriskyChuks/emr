from django.contrib import admin

from .models import MedicalService, PatientEncounterService, ServiceType

admin.site.register(MedicalService)

admin.site.register(PatientEncounterService)

admin.site.register(ServiceType)

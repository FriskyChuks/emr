from django.contrib import admin

from .models import EncounterRoute, PatientEncounter, DischargePatient


admin.site.register(PatientEncounter)

admin.site.register(EncounterRoute)

admin.site.register(DischargePatient)

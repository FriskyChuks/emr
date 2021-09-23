from django.contrib import admin

from .models import Diagnosis, DiagnosisType, MakeDiagosis


admin.site.register(Diagnosis)
admin.site.register(DiagnosisType)
admin.site.register(MakeDiagosis)


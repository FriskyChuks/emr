from django.contrib import admin

from .models import Diagnosis, MakeDiagnosis


admin.site.register(Diagnosis)
admin.site.register(MakeDiagnosis)


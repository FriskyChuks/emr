from django.contrib import admin

from .models import Diagnosis, MakeDiagosis


admin.site.register(Diagnosis)
admin.site.register(MakeDiagosis)


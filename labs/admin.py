from django.contrib import admin

from .models import LabUnit, CompoundTest, LabTest, LabRequest

admin.site.register(LabTest)

admin.site.register(CompoundTest)

admin.site.register(LabUnit)

admin.site.register(LabRequest)

from django.contrib import admin

from .models import *

admin.site.register(Continent)
admin.site.register(Patient)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(LGA)
admin.site.register(Relationship)

# admin.site.register(PatientImage)

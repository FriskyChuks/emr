from django.contrib import admin

from .models import RadiologyService, RaiseRadiologyService, RadiologyServiceType

admin.site.register(RadiologyServiceType)

admin.site.register(RadiologyService)

admin.site.register(RaiseRadiologyService)

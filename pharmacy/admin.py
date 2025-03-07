from django.contrib import admin

from .models import Item, Brand, Prescription, Dispensary


admin.site.register(Item)

admin.site.register(Brand)

admin.site.register(Prescription)

admin.site.register(Dispensary)

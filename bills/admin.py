from django.contrib import admin

from .models import Bill, Payment, Wallet


admin.site.register(Bill)
admin.site.register(Payment)
admin.site.register(Wallet)

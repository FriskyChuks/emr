from django import forms
from django.db import models

from .models import Bill, Payment


# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = Payment
#         fields = ['']
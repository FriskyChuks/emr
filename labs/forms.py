from django import forms
from django.contrib.admin import options
from django.forms import widgets
from bootstrap_datepicker_plus import DatePickerInput

from .models import LabResult


class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ["lab_request", "result"]
        # exclude = []

        widgets = {
            'result': forms.TextInput(attrs={'class': 'form-control'}),           
        }

from django import forms

from .models import MedicalService, PatientEncounterService #, NextOfKin, Address


class MedicalServiceForm(forms.ModelForm):
    class Meta:
        model = MedicalService
        fields = ["medical_service", "type"]

        widgets = {
                'medical_service': forms.TextInput(attrs={'class': 'form-control'}),
                'type': forms.Select(attrs={'class': 'form-control'}),
            }




class PatientEncounterServiceForm(forms.ModelForm):
    class Meta:
        model = PatientEncounterService
        fields = ["medical_service", "unit"]

        widgets = {
                'medical_service': forms.Select(attrs={'class': 'form-control'}),
                'unit': forms.NumberInput(attrs={'class': 'form-control'}),
            }
from django import forms
from django.forms import widgets

from .models import PatientEncounter, DischargePatient, EncounterRoute


class EncounterForm(forms.ModelForm):
    class Meta:
        model = PatientEncounter
        fields = ["current_clinic", "current_ward"]

        labels = {
        "current_clinic": "Select a Clinic",
        "current_ward": "Select a Ward",

        }

        widgets = {
            'current_clinic': forms.Select(attrs={'class': 'form-control'}),
            'current_ward': forms.Select(attrs={'class': 'form-control'}),
        }


class DischargeForm(forms.ModelForm):
    class Meta:
        model = DischargePatient
        # fields = ["current_clinic", "current_ward"]
        exclude = ['encounter_no', 'date_created', 'created_by']

        labels = {
        "discharge_type": "Type of Discharge",
        "created_by": "Discharged by",

        }

        widgets = {
            'discharge_type': forms.Select(attrs={'class': 'form-control'}),
            'reason_for_discharge': forms.Textarea(attrs={'class': 'form-control'}),
        }



class TransferForm(forms.ModelForm):
    class Meta:
        model = EncounterRoute
        fields = ["clinic", "ward"]
        # exclude = ['encounter_no', 'date_created', 'created_by']

        labels = {
        "clinic": "Select a Clinic",
        "ward": "Select a Ward",
        }

        widgets = {
            'clinic': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a clinic'}),
            'ward': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a ward'}),
        }

    # def clean_clinic(self):
    #     clinic = self.cleaned_data['clinic']
    #     if not clinic:
    #         raise forms.ValidationError("You need to select a location.")
    #     else:
    #         print("You need to select a location.")
    #         return clinic
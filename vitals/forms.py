from django import forms
from django.forms import widgets

from .models import PatientVitalSigns, PatientNotes


class VitalSignsForm(forms.ModelForm):
    class Meta:
        model = PatientVitalSigns
        fields = ["weight", "temperature", "blood_pressure", "pulse_rate", "sp_02"]
        # exclude = ["patient_encounter"]

        widgets = {
        'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        'temperature': forms.NumberInput(attrs={'class': 'form-control'}),
        'blood_pressure': forms.TextInput(attrs={'class': 'form-control'}),
        'pulse_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        'sp_02': forms.NumberInput(attrs={'class': 'form-control'}),
        }


    def clean(self):
        cleaned_data = super(VitalSignsForm, self).clean()
        weight = cleaned_data.get('weight')
        temperature = cleaned_data.get('temperature')
        blood_pressure = cleaned_data.get('blood_pressure')
        pulse_rate = cleaned_data.get('pulse_rate')
        sp_02 = cleaned_data.get('sp_02')
        if not weight:# or temperature:or not blood_pressure or not pulse_rate or not sp_02:
            raise forms.ValidationError('You have to write something!')


class PatientNotesForm(forms.ModelForm):
    class Meta:
        model = PatientNotes
        exclude = ["patient_encounter", "created_by"]

        widgets = {
            'note_type': forms.Select(attrs={'class': 'form-control'}),
            'sub_title': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
        }

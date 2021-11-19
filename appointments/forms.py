from django import forms
from .models import Appointment

class MyDateTimeInput(forms.DateTimeInput):
    input_type = 'date'

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["clinic", "appointment_date", "appointment_time", "reason"]

        widgets = {
            'clinic': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': MyDateTimeInput(attrs={'class': 'form-control'}),                            
            'appointment_time': forms.TimeInput(attrs={'type': 'time','class': 'form-control'}), 
            'reason': forms.TextInput(attrs={'class': 'form-control'}),           
        }


class UpdateAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["clinic", "appointment_date", "appointment_time", "reason"]

        widgets = {
            'clinic': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': MyDateTimeInput(attrs={'class': 'form-control'}),                            
            'appointment_time': forms.TimeInput(attrs={'type': 'time','class': 'form-control'}), 
            'reason': forms.TextInput(attrs={'class': 'form-control'}),           
        }
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
    def __init__(self, *args, **kwargs):
       super(UpdateAppointmentForm, self).__init__(*args, **kwargs)
       self.fields['patient'].widget.attrs['readonly'] = True

    class Meta:
        model = Appointment
        fields = ["patient","clinic", "appointment_date", "appointment_time", "reason"]

        widgets = {
            'patient': forms.TextInput(attrs={'class': 'form-control'}),
            'clinic': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': MyDateTimeInput(attrs={'class': 'form-control'}),                            
            'appointment_time': forms.TimeInput(attrs={'type': 'time','class': 'form-control'}), 
            'reason': forms.TextInput(attrs={'class': 'form-control'}),           
        }


        
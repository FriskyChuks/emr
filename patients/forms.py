from django import forms
from django.contrib.admin import options
from django.forms import widgets

from .models import *


# for DateTime input use
class MyDateTimeInput(forms.DateTimeInput):
    input_type = 'date'

# # for DateTime input use


class MyTimeInput(forms.TimeInput):
    input_type = 'date'


# # for Date input use
class MyDateInput(forms.DateInput):
    input_type = 'date'


class PatientBiodataForm(forms.ModelForm):
    class Meta:
        model = Patient
        # fields = ["first_name", "last_name", "other_names", "gender", "date_of_birth", "marital_status"]
        exclude = ["date_created", "last_updated",
                   "active", "created_by", "new"]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'other_names': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': MyDateInput(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'phone_1': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_2': forms.NumberInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'l_g_a': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'next_of_kin_relationship': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'next_of_kin_address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['state'].queryset = State.objects.none()


class PatientImageForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["foto"]


class UpdatePatientForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #    super(UpdatePatientForm, self).__init__(*args, **kwargs)
    #    self.fields['patient'].widget.attrs['readonly'] = True

    class Meta:
        model = Patient
        # fields = ["first_name", "last_name", "other_names", "gender", "date_of_birth", "marital_status"]
        exclude = ["", "date_created", "last_updated",
                   "active", "created_by", "new"]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'other_names': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': MyDateInput(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'phone_1': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_2': forms.NumberInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'l_g_a': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'next_of_kin_relationship': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'next_of_kin_address': forms.TextInput(attrs={'class': 'form-control'}),
        }

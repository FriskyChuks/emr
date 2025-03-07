from django import forms
from django.db import models

from .models import Item, Brand, Prescription


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item

        exclude = ['timestamp', 'updated', 'created_by', 'active']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Generic names like Paracetamol, Albendazole etc'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Brief description of the Item above'}), 
            'category': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            # 'strength': forms.NumberInput(attrs={'class': 'form-control'}),          
        }



class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand

        exclude = ['timestamp', 'updated', 'created_by', 'active']

        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Brand names like emzor, lumenfantrine etc'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Brief description of the brand above'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),           
            'sale_price': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription

        exclude = ['encounter_no','patient','timestamp', 'updated', 'created_by', 'active']

        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            # 'strength': forms.TextInput(attrs={'class': 'form-control'}),
            'qty_per_take': forms.NumberInput(attrs={'class': 'form-control'}),
            'times_daily': forms.NumberInput(attrs={'class': 'form-control'}),
            'no_of_days': forms.NumberInput(attrs={'class': 'form-control'}),
        }
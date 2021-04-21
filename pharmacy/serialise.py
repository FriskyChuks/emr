from django.db import models
from rest_framework import serializers
from .models import Prescription


class DrugPrescription(serializers.ModelSerializer):
    class Meta:
        models=Prescription
        fiels = "__all__"
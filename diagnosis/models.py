from re import T, U
from django.db import models

from locations.models import Clinic
from visits.models import PatientEncounter
from accounts.models import User


class Diagnosis(models.Model):
    title = models.CharField(max_length=225)
    clinic = models.ManyToManyField(Clinic)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title


# class DiagnosisType(models.Model):
#     type = models.CharField(max_length=20)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     date_created = models.DateTimeField(auto_now_add=True, auto_now=False)

#     class Meta:
#         ordering = ['type']

#     def __str__(self):
#         return self.type


class MakeDiagosis(models.Model):
    encounter = models.ForeignKey(PatientEncounter, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    # type = models.ForeignKey(DiagnosisType, on_delete=models.CASCADE)
    final = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.diagnosis
    

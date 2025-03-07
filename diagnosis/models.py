from django.db import models

from locations.models import Clinic
from visits.models import PatientEncounter
from accounts.models import User


class Diagnosis(models.Model):
    title = models.CharField(max_length=225)
    clinic = models.ManyToManyField(Clinic, blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class MakeDiagnosis(models.Model):
    encounter = models.ForeignKey(PatientEncounter, on_delete=models.CASCADE)
    icd = models.ForeignKey(
        Diagnosis, on_delete=models.CASCADE, blank=True, null=True)
    user_defined = models.CharField(max_length=225, blank=True, null=True)
    final = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        if self.icd:
            return str(self.icd)
        return str(self.user_defined)

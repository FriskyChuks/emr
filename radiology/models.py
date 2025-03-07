from django.db import models

from django.conf import settings

from visits.models import PatientEncounter
from patients.models import Patient

User = settings.AUTH_USER_MODEL


class RadiologyServiceType(models.Model):
    type                = models.CharField(max_length=150)
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date                = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.type


class RadiologyService(models.Model):
    radiology_service   = models.CharField(max_length=150)
    type                = models.ForeignKey(RadiologyServiceType, on_delete=models.CASCADE)
    price               = models.DecimalField(max_digits=65, decimal_places=2, default=00.00)
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date                = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.radiology_service)


class RadiologyRequest(models.Model):
    encounter_no        = models.ForeignKey(PatientEncounter, on_delete=models.CASCADE)
    patient             = models.ForeignKey(Patient, on_delete=models.CASCADE)
    radiology_service   = models.ForeignKey(RadiologyService, on_delete=models.CASCADE)
    clinical_info       = models.CharField(max_length=225, blank=True, null=True)
    decline             = models.BooleanField(default=False)
    done                = models.BooleanField(default=False)
    subtotal	        = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
    unit                = models.PositiveIntegerField(default=1)
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date                = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.radiology_service)



class RadiologyReport(models.Model):
    radiologyrequest = models.ForeignKey(RadiologyRequest, on_delete=models.CASCADE)
    findings = models.TextField()
    diagnosis = models.CharField(max_length=225, blank=True, null=True)
    other_findings = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.diagnosis)

from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from visits.models import PatientEncounter
from patients.models import Patient

from django.conf import settings

User = settings.AUTH_USER_MODEL


class ServiceType(models.Model):
    type                = models.CharField(max_length=150)
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date                = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.type


class MedicalService(models.Model):
    medical_service     = models.CharField(max_length=150)
    type                = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    price               = models.DecimalField(max_digits=65, decimal_places=2, default=00.00)
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created        = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.medical_service)# + "-->"+ str(self.price)


class PatientEncounterService(models.Model):
    encounter_no        = models.ForeignKey(PatientEncounter, on_delete=models.CASCADE)
    patient             = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medical_service     = models.ForeignKey(MedicalService, on_delete=models.CASCADE)
    subtotal	        = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
    unit                = models.PositiveIntegerField(default=1)
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date                = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.medical_service)

    
    # def get_sub_total(self):
    #     if self.date:
    #         new_sub_total=self.medical_service.price * self.unit
    #         self.subtotal = new_sub_total
    #         self.save()



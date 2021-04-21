from django.conf import settings
from django.db import models

from visits.models import PatientEncounter
from patients.models import Patient
from medical_services.models import PatientEncounterService
from pharmacy.models import Prescription
from radiology.models import RaiseRadiologyService

User = settings.AUTH_USER_MODEL


BILL_STATUS = (
    ("pending","Pending"),
    ("billed","Billed"),
    ("paid","Paid")
)


PAY_ACTION = (
    ("deposit","Deposit"),
    ("invoice","Invoice"),
    ("receipt","Receipt"),
)


class Bill(models.Model):
    encounter           = models.ForeignKey(PatientEncounter, on_delete=models.CASCADE)
    patient             = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medical_service     = models.ForeignKey(PatientEncounterService, on_delete=models.CASCADE, blank=True, null=True)
    radiology_service   = models.ForeignKey(RaiseRadiologyService, on_delete=models.CASCADE, blank=True, null=True)
    prescription        = models.ForeignKey(Prescription, on_delete=models.CASCADE, blank=True, null=True)
    status              = models.CharField(max_length=10, choices=BILL_STATUS, default='pending')
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created        = models.DateTimeField(auto_now_add=False, auto_now=True)
    last_updated        = models.DateTimeField(auto_now_add=True, auto_now=False)


class Payment(models.Model):
    bill            = models.ForeignKey(Bill, on_delete=models.CASCADE)
    amount_paid     = models.DecimalField(decimal_places=2, default='00.00', max_digits=20)
    action          = models.CharField(max_length=20, choices=PAY_ACTION)
    created_by      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created    = models.DateTimeField(auto_now_add=False, auto_now=True)
    last_updated    = models.DateTimeField(auto_now_add=True, auto_now=False)


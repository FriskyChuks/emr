from django.conf import settings
from django.db import models

from visits.models import PatientEncounter
from patients.models import Patient
from medical_services.models import PatientEncounterService
from pharmacy.models import Prescription
from radiology.models import RaiseRadiologyService
from labs.models import LabRequest

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
    lab_request          = models.ForeignKey(LabRequest, on_delete=models.CASCADE, blank=True, null=True)
    status              = models.CharField(max_length=10, choices=BILL_STATUS, default='pending')
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created        = models.DateTimeField(auto_now_add=False, auto_now=True)
    last_updated        = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        if self.medical_service:
            return f"{self.medical_service} | {self.encounter.patient.id}"
        elif self.radiology_service:
            return f"{self.radiology_service} | {self.encounter.patient.id}"
        elif self.lab_request:
            return f"{self.lab_request} | {self.encounter.patient.id}"
        else:
            return f"{self.prescription} | {self.encounter.patient.id}"


class Payment(models.Model):
    bill            = models.ForeignKey(Bill, on_delete=models.CASCADE)
    amount_paid     = models.DecimalField(decimal_places=2, default='00.00', max_digits=20)
    action          = models.CharField(max_length=20, choices=PAY_ACTION)
    created_by      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created    = models.DateTimeField(auto_now_add=False, auto_now=True)
    last_updated    = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        if self.bill.medical_service:
            return f"{self.bill.medical_service} {self.amount_paid}"
        else:
            return f"{self.bill.radiology_service} {self.amount_paid}"


class Wallet(models.Model):
    patient         = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    account_balance = models.DecimalField(decimal_places=2, default='00.00', max_digits=20)
    created_by      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_created    = models.DateTimeField(auto_now_add=False, auto_now=True)
    last_updated    = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f"N{self.account_balance} || {self.patient.id}"




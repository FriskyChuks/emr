from locations.models import Clinic, Ward
from patients.models import Patient
from django.db.models.signals import post_save
from django.urls import reverse
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# from django.contrib.auth.models import User


TYPE_OF_DISCHARGE = (
    ('regular', 'Regular Discharge'),
    ('against medical advice', 'Against Medical Advice'),
    # ('regular discharge', 'Regular Discharge'),
)


class PatientEncounter(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, blank=True, null=True)
    current_clinic = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, blank=True, null=True)
    current_ward = models.ForeignKey(
        Ward, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=True)
    pay_status = models.BooleanField(default=0)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        if self.current_ward:
            return str(self.id) + " " + str(self.current_ward)
        else:
            return str(self.id) + " " + str(self.current_clinic)

    def get_absolute_url(self):
        return reverse("clinic_visits_display", kwargs={"current_clinic_id": self.current_clinic_id})


class EncounterRoute(models.Model):
    encounter_no = models.ForeignKey(
        PatientEncounter, on_delete=models.CASCADE)
    clinic = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, blank=True, null=True)
    ward = models.ForeignKey(
        Ward, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        if self.clinic:
            return str(self.encounter_no.id) + "-->" + str(self.clinic)
        else:
            return str(self.encounter_no.id) + "-->" + str(self.ward)


class DischargePatient(models.Model):
    encounter_no = models.ForeignKey(
        PatientEncounter, on_delete=models.CASCADE)
    discharge_type = models.CharField(max_length=50, choices=TYPE_OF_DISCHARGE)
    reason_for_discharge = models.CharField(
        max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.discharge_type

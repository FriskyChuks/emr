from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User

User = settings.AUTH_USER_MODEL

from visits.models import PatientEncounter


NOTE_TYPES = (
		('nursing_note', 'Nursing Notes'),
		('daily_round', 'Daily Rounds'),
        ('physical_examination', 'Physical Examination'),
        ('patient_history', 'Patient History'),
		('anaesthetic_note', 'Anaesthetic Notes'),
        ('intervention', 'Intervention'),
	)


class PatientVitalSigns(models.Model):
    patient_encounter    = models.ForeignKey(PatientEncounter, on_delete=models.CASCADE)
    weight          = models.DecimalField(decimal_places=2, max_digits=50, blank=True, null=True)
    temperature     = models.DecimalField(decimal_places=2, max_digits=50, blank=True, null=True)
    blood_pressure  = models.CharField(max_length=10, blank=True, null=True)
    pulse_rate      = models.DecimalField(decimal_places=2, max_digits=50, blank=True, null=True)
    sp_02           = models.DecimalField(decimal_places=2, max_digits=50, blank=True, null=True)
    created_by      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date            = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated         = models.DateTimeField(auto_now_add=False, auto_now=True)


class PatientNotes(models.Model):
    patient_encounter    = models.ForeignKey(PatientEncounter, on_delete=models.CASCADE)
    note_type             = models.CharField(max_length=50, choices=NOTE_TYPES)
    sub_title             = models.CharField(max_length=100)
    note                  = models.TextField()
    date                  = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated               = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_by            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


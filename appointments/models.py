from django.db import models
from django.conf import settings

from patients.models import Patient
from locations.models import Clinic

User = settings.AUTH_USER_MODEL

APPT_STATUS = (
		('pending', 'pending'),
		('seen', 'seen'),
		('cancelled', 'cancelled'),
	)

class Appointment(models.Model):
	patient				= models.ForeignKey(Patient, on_delete=models.CASCADE)
	clinic				= models.ForeignKey(Clinic, on_delete=models.CASCADE)
	appointment_date	= models.DateField()
	appointment_time	= models.TimeField()
	reason 				= models.CharField(max_length=100, blank=True, null=True)
	date_created    	= models.DateTimeField(auto_now_add=True, auto_now=False)
	status				= models.CharField(max_length=10, choices=APPT_STATUS, default='pending')
	last_updated    	= models.DateTimeField(auto_now_add=False, auto_now=True)
	active          	= models.BooleanField(default=True)
	created_by      	= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return str(self.patient.id) + ", "+ str(self.patient) + " ==> " + str(self.appointment_date)


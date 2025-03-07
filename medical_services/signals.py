from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver

from visits.models import PatientEncounter
from .models import PatientEncounterService, MedicalService


@receiver(post_save, sender=PatientEncounterService)
def post_save_update_sub_total(sender, instance, created, **kwargs):
    if created:
        price = instance.medical_service.price
        qty = instance.unit
        new_subtotal = price * qty
        PatientEncounterService.objects.filter(id=instance.id).update(subtotal=new_subtotal)


@receiver(post_save, sender=PatientEncounter)
def post_save_create_consultation_bill(sender, instance, created, **kwargs):
    if created:
        encounter = PatientEncounter.objects.filter(id=instance.id)
        for e in encounter:
            if e.patient.new:
                PatientEncounterService.objects.create(
                    encounter_no_id    = instance.id,
                    patient_id          = instance.patient.id,
                    medical_service_id  = 1, # Registration
                    unit                = 1,
                    created_by_id       = instance.created_by.id
                )
            else:         
                PatientEncounterService.objects.create(
                    encounter_no_id    = instance.id,
                    patient_id          = instance.patient.id,
                    medical_service_id  = 2, # Consultation
                    unit                = 1,
                    created_by_id       = instance.created_by.id
                )
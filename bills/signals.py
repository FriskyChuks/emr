from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver

from visits.models import PatientEncounter
from medical_services.models import PatientEncounterService
from pharmacy.models import Prescription
from radiology.models import RaiseRadiologyService

from .models import Bill

# Radiology Bill
@receiver(post_save, sender=RaiseRadiologyService)
def post_save_radiology_bill(sender, instance, created, **kwargs):
    if created:
        # print(created)
        # print("ID = ", instance.id)
        # print("Encounter No =", instance.encounter_no_id)
        # print("sender =", sender)

        Bill.objects.create(
            encounter_id = instance.encounter_no_id,
            patient_id = instance.patient_id,
            radiology_service_id = instance.id,
            status = "pending",
            created_by_id = instance.created_by_id           
        )


# Medical Service Bill
@receiver(post_save, sender=PatientEncounterService)
def post_save_medical_service_bill(sender, instance, created, **kwargs):
    if created:
        if instance.medical_service.medical_service == "Consultation":
            Bill.objects.create(
                encounter_id = instance.encounter_no_id,
                patient_id = instance.patient_id,
                medical_service_id = instance.id,
                status = "billed",
                created_by_id = instance.created_by_id           
            )
        else:
            Bill.objects.create(
            encounter_id = instance.encounter_no_id,
            patient_id = instance.patient_id,
            medical_service_id = instance.id,
            status = "pending",
            created_by_id = instance.created_by_id           
        )


# Pharmacy Bill
@receiver(post_save, sender=Prescription)
def post_save_pharmacy_bill(sender, instance, created, **kwargs):
    if created:
        Bill.objects.create(
            encounter_id = instance.encounter_no_id,
            patient_id = instance.patient_id,
            prescription_id = instance.id,
            status = "pending",
            created_by_id = instance.created_by_id           
        )
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver

from visits.models import PatientEncounter
from medical_services.models import PatientEncounterService
from pharmacy.models import Prescription
from radiology.models import RaiseRadiologyService
from labs.models import LabRequest
from patients.models import Patient

from .models import Bill, Wallet

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


# LAB Bill
@receiver(post_save, sender=LabRequest)
def post_save_lab_request_bill(sender, instance, created, **kwargs):
    if created:
        Bill.objects.create(
            encounter_id = instance.encounter_id,
            patient_id = instance.patient_id,
            lab_request_id = instance.id,
            status = "pending",
            created_by_id = instance.created_by_id           
        )


@receiver(post_save, sender=Patient)
def post_save_load_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(patient_id=instance.id)
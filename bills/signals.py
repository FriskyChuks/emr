from django.db.models.signals import post_save
from django.dispatch import receiver

from visits.models import PatientEncounter
from medical_services.models import PatientEncounterService
from pharmacy.models import Dispensary
from radiology.models import RadiologyRequest
from labs.models import LabRequest
from patients.models import Patient

from .models import Bill, Wallet

# Radiology Bill


@receiver(post_save, sender=RadiologyRequest)
def post_save_radiology_bill(sender, instance, created, **kwargs):
    if created:
        Bill.objects.create(
            encounter_id=instance.encounter_no_id,
            # patient_id = instance.patient_id,
            radiology_service_id=instance.id,
            status="pending",
            created_by_id=instance.created_by_id
        )


# Medical Service Bill
@receiver(post_save, sender=PatientEncounterService)
def post_save_medical_service_bill(sender, instance, created, **kwargs):
    if created:
        if instance.medical_service.medical_service == "Consultation" or instance.medical_service.medical_service == "Registration":
            new_bill = Bill.objects.create(
                encounter_id=instance.encounter_no_id,
                # patient_id = instance.patient_id,
                medical_service_id=instance.id,
                status="billed",
                created_by_id=instance.created_by_id
            )
            bill_id = new_bill.id
            service_price = instance.medical_service.price

            wallet = Wallet.objects.get(patient_id=instance.patient_id)
            wallet_balance = wallet.account_balance
            if wallet_balance >= service_price:
                wallet_balance -= service_price
                wallet = Wallet.objects.filter(patient_id=instance.patient_id).update(
                    account_balance=wallet_balance)
                Bill.objects.filter(id=bill_id).update(status="paid")
        else:
            Bill.objects.create(
                encounter_id=instance.encounter_no_id,
                # patient_id = instance.patient_id,
                medical_service_id=instance.id,
                status="pending",
                created_by_id=instance.created_by_id
            )


# Pharmacy Bill
@receiver(post_save, sender=Dispensary)
def post_save_pharmacy_bill(sender, instance, created, **kwargs):
    if created:
        Bill.objects.create(
            encounter_id=instance.prescription.encounter_no.id,
            # patient_id = instance.prescription.patient.id,
            dispensary_id=instance.id,
            status="billed",
            created_by_id=instance.created_by_id
        )


# LAB Bill
@receiver(post_save, sender=LabRequest)
def post_save_lab_request_bill(sender, instance, created, **kwargs):
    if created:
        Bill.objects.create(
            encounter_id=instance.encounter_id,
            # patient_id = instance.patient_id,
            lab_request_id=instance.id,
            status="pending",
            created_by_id=instance.created_by_id
        )


@receiver(post_save, sender=Patient)
def post_save_create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(patient_id=instance.id)

from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import DischargePatient, EncounterRoute, PatientEncounter


@receiver(post_save, sender=EncounterRoute)
def post_save_update_patient_encounter(sender, instance, created, **kwargs):
    if created:
        if instance.clinic_id:
            PatientEncounter.objects.filter(id=instance.encounter_no.id, active=True).update(
                                                                                current_clinic = instance.clinic,
                                                                                current_ward   = None
                                                                            )
        else:
            PatientEncounter.objects.filter(id=instance.encounter_no.id, active=True).update(
                                                                                current_clinic = None,
                                                                                current_ward   = instance.ward
                                                                            )


@receiver(post_save, sender=PatientEncounter)
def post_save_create_encounter_route(sender, instance, created, **kwargs):
    if created:
        if instance.current_clinic_id:
            EncounterRoute.objects.create(
                encounter_no_id = instance.id,
                clinic_id = instance.current_clinic_id,
                created_by_id = instance.created_by_id           
            )
        else:
            if instance.current_ward_id:
                EncounterRoute.objects.create(
                    encounter_no_id = instance.id,
                    ward_id = instance.current_ward_id,
                    created_by_id = instance.created_by_id           
                )

from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import DischargePatient, EncounterRoute, PatientEncounter


@receiver(post_save, sender=EncounterRoute)
def post_save_update_patient_encounter(sender, instance, created, **kwargs):
    if created:
        # print(instance.ward_id)
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
        # print(created)
        # print(instance.id)
        # print(instance.current_clinic)
        # print(sender)

        # EncounterRoute.objects.update(
        #     encounter_no_id = instance.id,
        #     clinic_id = instance.current_clinic_id,
        #     ward_id = instance.current_ward_id            
        # )

        EncounterRoute.objects.create(
            encounter_no_id = instance.id,
            clinic_id = instance.current_clinic_id,
            ward_id = instance.current_ward_id,
            created_by_id = instance.created_by_id           
        )



@receiver(post_save, sender=DischargePatient)
def post_save_discharge_patient(sender, instance, created, **kwargs):
    if created:
        print(created)
        print(instance)
        print(sender)

        PatientEncounter.objects.filter(id=instance.encounter_no.id, active=True).update(active=False)
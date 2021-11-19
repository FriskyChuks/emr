# from django.db.models.deletion import SET_NULL
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from patients.models import Patient

# from .models import User


# @receiver(post_save, sender=Patient)
# def post_save_update_sub_total(sender, instance, created, **kwargs):
#     if created:
#         User.objects.create(
#             username        = instance.id,
#             password        = ("password"),
#             first_name      = instance.first_name,
#             last_name       = instance.last_name,
#             other_names     = instance.other_names,
#             is_a_patient    = True
#         )

#         new_user = User.objects.get(username=instance.id)
#         new_user.set_password("pass")
#         new_user.save()
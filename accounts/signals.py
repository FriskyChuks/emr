from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def post_save_update_sub_total(sender, instance, created, **kwargs):
    if created:
        User.objects.filter(id=instance.id).update(group_id=1) # users
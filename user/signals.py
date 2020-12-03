from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()

@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        if instance.first_name:
            models.UserProfile.objects.create(user=instance, name=instance.first_name)
        else:
            models.UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
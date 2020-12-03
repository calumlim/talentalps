from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models

@receiver(post_save, sender=models.JobListing)
def create_questionnaire(sender, instance, created, **kwargs):
    if created:
        models.Questionnaire.objects.create(joblisting=instance)

@receiver(post_save, sender=models.JobListing)
def save_user_profile(sender, instance, **kwargs):
    instance.questionnaire.save()
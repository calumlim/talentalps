from celery import Celery
from celery import shared_task
from celery.schedules import crontab
from django.db import transaction

from . import models
from talentalps.celery import app

@app.task
def increase_view(pk):
    try:
        listing = models.JobListing.objects.get(pk=pk)
        listing.views += 1
        listing.save()
    except:
        return False
    return True

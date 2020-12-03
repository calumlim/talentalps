from celery import Celery
from celery import shared_task
from celery.schedules import crontab
from django.db import transaction

import json

from user import models as user_models
from talentalps.celery import app

@app.task
def update_company_image_order(new_order, company_pk):
    company_images = user_models.CompanyImage.objects.filter(company__pk=company_pk).only('order').order_by('order')
    order = json.loads(new_order)
    try:
        with transaction.atomic():
            for i in range(len(company_images)):
                pos = int(order['order'][i]) - 1
                if company_images[pos].order != i+1:
                    company_images[pos].order = i+1
                    company_images[pos].save()
    except:
        return False
    return True

@app.task
def delete_company_image(image_pk, company_pk):
    image = user_models.CompanyImage.objects.get(pk=image_pk, company__pk=company_pk)
    try:
        image.delete()
        image_set = user_models.CompanyImage.objects.filter(company__pk=company_pk)
        for i in range(len(image_set)):
            image_set[i].order = i + 1
            image_set[i].save()

    except:
        return False
    return True
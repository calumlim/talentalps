from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.Candidate)
admin.site.register(models.Company)
admin.site.register(models.CompanyImage)
from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.JobListing)
admin.site.register(models.JobApplication)
admin.site.register(models.Questionnaire)
admin.site.register(models.Questions)
admin.site.register(models.CandidateQuestionnaireAnswer)
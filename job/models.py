from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from ckeditor.fields import RichTextField

from decimal import Decimal

from django.contrib.auth.models import User
from talentalps.models import BaseModel
from talentalps import constants

# Create your models here.
class JobListing(BaseModel):
    title = models.CharField(_("title"), max_length=100)
    state = models.CharField(_("state"), max_length=80, choices=constants.STATE)
    country = models.CharField(_("country"), max_length=80, choices=constants.COUNTRY)
    industry = models.CharField(_("industry"), max_length=80, choices=constants.INDUSTRY)
    employment_type = models.CharField(_("employment type"), max_length=60, choices=constants.EMPLOYMENT_TYPE_CHOICES)
    description = RichTextField(config_name='job_listing_editor', max_length=1800)
    level = models.CharField(_("level"), max_length=50, choices=constants.LEVEL)
    specialisation = ArrayField(ArrayField(models.CharField(_("specialisation"), max_length=80)), size=5)
    qualifications = ArrayField(ArrayField(models.CharField(_("qualifications"), max_length=80)), size=5)
    pay_from = models.DecimalField(_("pay_from"), max_digits=8, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    pay_to = models.DecimalField(_("pay_to"), max_digits=8, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    years_of_experience = models.PositiveIntegerField(_("years of experience"))
    keywords = ArrayField(ArrayField(models.CharField(_("keywords"), max_length=80)), size=10)
    recommended = models.BooleanField(_("recommended"), default=False)
    recommended_start_timestamp: models.DateTimeField(_("recommended start timestamp"), auto_now=False, auto_now_add=False, null=True, blank=True)
    views = models.PositiveIntegerField(_("views"))
    expired = models.BooleanField(_("expired"), default=False)

    company = models.ForeignKey("user.Company", verbose_name=_("company"), on_delete=models.CASCADE)

    def increase_view(self):
        self.views += 1
        self.save()

class JobApplication(BaseModel):
    STATUS_PENDING = 'pending'
    STATUS_INTERVIEW_SET = 'interview'
    STATUS_COMPLETED = 'complete'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_INTERVIEW_SET, 'Interview Set'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_REJECTED, 'Rejected'),
    )

    status = models.CharField(_("status"), max_length=50, choices=STATUS_CHOICES, default=STATUS_PENDING)
    feedback = models.TextField(_("feedback"), max_length=300)

    candidate = models.ForeignKey("user.Candidate", verbose_name=_("candidate"), on_delete=models.CASCADE)
    joblisting = models.ForeignKey("JobListing", verbose_name=_("job listing"), on_delete=models.CASCADE)

class Interview(BaseModel):
    TYPE_VIRTUAL = 'virtual'
    TYPE_MEETUP = 'meetup'
    TYPE_OTHER = 'other'
    TYPE_CHOICES = (
        (TYPE_VIRTUAL, 'Virtual/Online Interview'),
        (TYPE_MEETUP, 'In Person Interview'),
        (TYPE_OTHER, 'Other'),
    )

    datetime = models.DateTimeField(_("date time"), auto_now=False, auto_now_add=False, null=True, blank=True)
    interview_type = models.CharField(_("interview type"), max_length=80, choices=TYPE_CHOICES)
    location = models.TextField(_("location"), max_length=200, null=True, blank=True)
    instructions = models.TextField(_("instructions"), max_length=500)

    candidate = models.ForeignKey("user.Candidate", verbose_name=_("candidate"), on_delete=models.CASCADE)
    jobapplication = models.ForeignKey("JobApplication", verbose_name=_("job application"), on_delete=models.CASCADE)

class Questionnaire(BaseModel):
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"), max_length=500)

    joblisting = models.OneToOneField("JobListing", verbose_name=_("job listing"), on_delete=models.CASCADE)

class Question(BaseModel):
    question = models.TextField(_("question"), max_length=300)

    questionnaire = models.ForeignKey("Questionnaire", verbose_name=_("questionnaire"), on_delete=models.CASCADE)

class CandidateQuestionnaireAnswer(BaseModel):
    question = models.TextField(_("question"), max_length=300)
    answer = models.TextField(_("answer"), max_length=400)

    candidate = models.ForeignKey("user.Candidate", verbose_name=_("candidate"), on_delete=models.CASCADE)
    jobapplication = models.ForeignKey("JobApplication", verbose_name=_("job application"), on_delete=models.CASCADE)
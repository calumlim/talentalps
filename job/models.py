from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from ckeditor.fields import RichTextField

from decimal import Decimal
import uuid
import datetime

from django.contrib.auth.models import User
from talentalps.models import BaseModel
from talentalps import constants
from . import tasks

# Create your models here.
class JobListing(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("title"), max_length=100)
    state = models.CharField(_("state"), max_length=80, choices=constants.STATE)
    country = models.CharField(_("country"), max_length=80, choices=constants.COUNTRY)
    industry = models.CharField(_("industry"), max_length=500)
    employment_type = models.CharField(_("employment type"), max_length=60, choices=constants.EMPLOYMENT_TYPE_CHOICES)
    description = RichTextField(config_name='job_listing_editor')
    responsibilities_description = RichTextField(config_name='job_listing_editor')
    requirements_description = RichTextField(config_name='job_listing_editor')
    level = models.CharField(_("level"), max_length=50, choices=constants.LEVEL)
    job_functions = models.CharField(_("job functions"), max_length=500)
    pay_from = models.DecimalField(_("pay_from"), max_digits=8, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    pay_to = models.DecimalField(_("pay_to"), max_digits=8, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    years_of_experience = models.PositiveIntegerField(_("years of experience"))
    recommended = models.BooleanField(_("recommended"), default=False)
    recommended_start_timestamp = models.DateTimeField(_("recommended start timestamp"), auto_now=False, auto_now_add=False, null=True, blank=True)
    views = models.PositiveIntegerField(_("views"), default=0)
    expiry_date = models.DateTimeField(_("expiry date"), default=datetime.datetime.now() + datetime.timedelta(days=30))
    expired = models.BooleanField(_("expired"), default=False)
    published = models.BooleanField(_("published"), default=False)

    company = models.ForeignKey("user.Company", verbose_name=_("company"), on_delete=models.CASCADE)
    userprofile = models.ForeignKey("user.UserProfile", verbose_name=_("user profile"), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.company})'
    
    @property
    def get_job_applications_count(self):
        return JobApplication.objects.filter(joblisting__pk=self.pk).count()

    def increase_view(self):
        tasks.increase_view(self.pk)

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
    joblisting = models.OneToOneField("JobListing", verbose_name=_("job listing"), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.joblisting}"

class Question(BaseModel):
    question = models.TextField(_("question"), max_length=120, blank=True)

    questionnaire = models.ForeignKey("Questionnaire", verbose_name=_("questionnaire"), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question} - {self.questionnaire.joblisting}"

class CandidateQuestionnaireAnswer(BaseModel):
    question = models.TextField(_("question"), max_length=300)
    answer = models.TextField(_("answer"), max_length=400)

    candidate = models.ForeignKey("user.Candidate", verbose_name=_("candidate"), on_delete=models.CASCADE)
    jobapplication = models.ForeignKey("JobApplication", verbose_name=_("job application"), on_delete=models.CASCADE)
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth.models import User
from talentalps.models import BaseModel
from talentalps import constants

def get_avatar_image_path(instance, filename):
    filename = f"0{filename[filename.find('.'):]}"
    return f"{instance.user.username}/avatar/{filename}"
def get_header_image_path(instance, filename):
    filename = f"0{filename[filename.find('.'):]}"
    return f"{instance.user.username}/header/{filename}"
def get_company_avatar_image_path(instance, filename):
    filename = f"0{filename[filename.find('.'):]}"
    print(filename)
    return f"employer/company/{instance.company_name}/avatar/{filename}"
def get_company_header_image_path(instance, filename):
    filename = f"0{filename[filename.find('.'):]}"
    return f"employer/company/{instance.company_name}/header/{filename}"

# Create your models here.
class UserProfile(BaseModel):
    name = models.CharField(_('name'), max_length=100, null=True, blank=True)
    address = models.CharField(_('address'), max_length=200, null=True, blank=True)
    postcode = models.PositiveIntegerField(_('postcode'), null=True, blank=True)
    state = models.CharField(_('state'), max_length=100, null=True, blank=True, choices=constants.STATE)
    country = models.CharField(_("country"), max_length=50, null=True, blank=True, choices=constants.COUNTRY)
    contact = models.CharField(_('contact'), max_length=15, null=True, blank=True)
    is_employer = models.BooleanField(_('is employer'), default=False)
    avatar = models.ImageField(_('avatar'), upload_to=get_avatar_image_path, null=True, blank=True)
    header = models.ImageField(_('header'), upload_to=get_header_image_path, null=True, blank=True)
    verified = models.BooleanField(_("verified"), default=False)
    receive_updates = models.BooleanField(_("receive updates"), default=False)

    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.user.username
    
class SearchHistory(BaseModel):
    history = ArrayField(ArrayField(models.CharField(_("history"), max_length=100, blank=True, null=True)), null=True, blank=True, size=10)

    userprofile = models.OneToOneField("UserProfile", verbose_name=_("user profile"), on_delete=models.CASCADE)

class SavedItem(BaseModel):
    joblisting = models.ForeignKey("job.JobListing", verbose_name=_("job listing"), on_delete=models.CASCADE)
    userprofile = models.ForeignKey("UserProfile", verbose_name=_("user profile"), on_delete=models.CASCADE)

class Candidate(BaseModel):
    SEEKING_ACTIVE = 'active'
    SEEKING_LOOKING = 'looking'
    SEEKING_CHOICES = (
        (SEEKING_ACTIVE, _('Actively Seeking')),
        (SEEKING_LOOKING, _('Just looking around')),
    )

    gender = models.CharField(_('gender'), max_length=10, choices=constants.GENDER)
    state = models.CharField(_('state'), max_length=100, choices=constants.STATE)
    nationality = models.CharField(_('nationality'), max_length=50, choices=constants.COUNTRY, default='MY')
    description = models.TextField(_('description'), max_length=1200, null=True, blank=True)
    seeking_status = models.CharField(_('seeking status'), max_length=50, choices=SEEKING_CHOICES)
    boost = models.BooleanField(_('boost'), default=False)

    userprofile = models.OneToOneField('UserProfile', on_delete=models.PROTECT)

class Company(BaseModel):
    SIZE_10 = '1 - 10'
    SIZE_50 = '10 - 50'
    SIZE_250 = '50 - 250'
    SIZE_500 = '250 - 500'
    SIZE_1000 = '500 - 1000'
    SIZE_5000 = '1000 - 5000'
    SIZE_10000 = '5000 - 10000'
    SIZE_10000_MORE = '10000+'
    SIZE_CHOICES = (
        (SIZE_10, '1 - 10 Employees'),
        (SIZE_50, '10 - 50 Employees'),
        (SIZE_250, '50 - 250 Employees'),
        (SIZE_500, '250 - 500 Employees'),
        (SIZE_1000, '500 - 1,000 Employees'),
        (SIZE_5000, '1,000 - 5,000 Employees'),
        (SIZE_10000, '5,000 - 10,000 Employees'),
        (SIZE_10000_MORE, '10,000+ Employees'),
    )

    TYPE_SOLE = 'sole_proprietorship'
    TYPE_PARTNERSHIP = 'partnership'
    TYPE_LLP = 'LLP'
    TYPE_SDN_BHD = 'SDN_BHD'
    TYPE_BERHAD = 'public_limited'
    TYPE_GUARANTEE = 'guarantee'
    TYPE_FOREIGN = 'foreign'
    TYPE_CHOICES = (
        (TYPE_SOLE, 'Sole Proprietorship'),
        (TYPE_PARTNERSHIP, 'Partnership'),
        (TYPE_LLP, 'Limited Liability Partnership (LLP)'),
        (TYPE_SDN_BHD, 'Private Limited Company (SDN BHD)'),
        (TYPE_BERHAD, 'Public Limited Company'),
        (TYPE_GUARANTEE, 'Company Limited By Guarantee'),
        (TYPE_FOREIGN, 'Foreign Company'),
    )

    avatar = models.ImageField(_('avatar'), upload_to=get_company_avatar_image_path, null=True, blank=True)
    company_name = models.CharField(_('company_name'), max_length=150)
    description = models.TextField(_('description'))
    website = models.CharField(_('website'), max_length=1000)
    company_size = models.CharField(_("company size"), max_length=50, choices=SIZE_CHOICES)
    company_type = models.CharField(_("type"), max_length=50, choices=TYPE_CHOICES)
    founded = models.PositiveIntegerField(_("founded"))
    header_image = models.ImageField(_("header image"), upload_to=get_company_header_image_path, null=True, blank=True)
    industry = models.CharField(_("industry"), max_length=150)
    other_industry = models.CharField(_("other industry"), max_length=100, null=True, blank=True)

    address = models.CharField(_('address'), max_length=200, null=True, blank=True)
    postcode = models.PositiveIntegerField(_('postcode'), null=True, blank=True)
    state = models.CharField(_('state'), max_length=100, null=True, blank=True, choices=constants.STATE)
    country = models.CharField(_('country'), max_length=100, null=True, blank=True, choices=constants.COUNTRY)

    userprofile = models.ForeignKey("UserProfile", verbose_name=_("user profile"), on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.company_name}'


class DailyStats(BaseModel):
    totaltraffic = models.PositiveIntegerField(_("total traffic"))
    uniqueusers: models.PositiveIntegerField(_("unique users"))
    jobapplications: models.PositiveIntegerField(_("job applications"))
    overallperformance: models.DecimalField(_("overall performance"), max_digits=5, decimal_places=2)

    company = models.ForeignKey("Company", verbose_name=_("company"), on_delete=models.CASCADE)
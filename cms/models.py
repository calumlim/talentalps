from django.db import models
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField

from talentalps.models import BaseModel

def get_announcement_image_path(instance, filename):
    return f"employer_announcement/{instance.title}/{filename}"

# Create your models here.
class FAQQuestions(BaseModel):
    question = models.CharField(_("question"), max_length=200)
    answer = RichTextField(max_length=1000)

class GeneralAnnouncement(BaseModel):
    title = RichTextField(max_length=250)
    link = models.TextField(_("link"))

class EmployerAnnouncement(BaseModel):
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"))
    image = models.ImageField(_("image"), upload_to=get_announcement_image_path, height_field=None, width_field=None, max_length=None, null=True, blank=True)
    link = models.TextField(_("link"))

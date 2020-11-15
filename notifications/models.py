from django.db import models
from django.utils.translation import ugettext_lazy as _

from talentalps.models import BaseModel

# Create your models here.
class JobApplicationNotification(BaseModel):
    TYPE_INTERVIEW = 'interview'
    TYPE_APPROVED = 'approved'
    TYPE_DECLINED = 'declined'
    TYPE_CHOICES = (
        (TYPE_INTERVIEW, 'Interview has been set!'),
        (TYPE_APPROVED, 'Job Application has been approved!'),
        (TYPE_DECLINED, 'Unfortunately, your job application has been declined.')
    )

    type = models.CharField(_("type"), max_length=100, choices=TYPE_CHOICES)
    message = models.CharField(_("message"), max_length=200)
    seen = models.BooleanField(_("seen"), default=False)

    jobapplication = models.ForeignKey("job.JobApplication", verbose_name=_("job application"), on_delete=models.CASCADE)
    user = models.ForeignKey("user.UserProfile", verbose_name=_("user"), on_delete=models.CASCADE)

    def seen(self):
        self.seen = True
        self.save()
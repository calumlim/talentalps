from django.db import models
from django.utils.translation import ugettext_lazy as _

from talentalps.models import BaseModel

# Create your models here.
class JobApplicationNotification(BaseModel):
    message = models.CharField(_("message"), max_length=200)
    seen = models.BooleanField(_("seen"), default=False)

    jobapplication = models.ForeignKey("job.JobApplication", verbose_name=_("job application"), on_delete=models.CASCADE)
    user = models.ForeignKey("user.UserProfile", verbose_name=_("user"), on_delete=models.CASCADE)

    def seen(self):
        self.seen = True
        self.save()
from django import forms

from . import models

class JobListingCreateForm(forms.ModelForm):

    class Meta:
        model = models.JobListing
        fields = ['title', 'state', 'country', 'industry', 'employment_type',
    'level', 'job_functions', 'pay_from', 'pay_to', 'years_of_experience',
    'company']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['industry'].choices = self.fields['industry'].choices[1:]
        self.fields['job_functions'].choices = self.fields['job_functions'].choices[1:]
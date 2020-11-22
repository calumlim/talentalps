from django import forms

from . import models
from talentalps import constants

class JobListingCreateForm(forms.ModelForm):

    class Meta:
        model = models.JobListing
        fields = ['title', 'state', 'country', 'industry', 'employment_type',
    'level', 'job_functions', 'pay_from', 'pay_to', 'years_of_experience',
    'company']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['industry'] = forms.MultipleChoiceField(choices=constants.INDUSTRY)
        self.fields['job_functions'] = forms.MultipleChoiceField(choices=constants.JOB_FUNCTIONS)
        self.fields['state'].required = False
        self.fields['country'].initial = 'MY'
    
    def clean_industry(self):
        return ', '.join(self.cleaned_data.get('industry'))
    
    def clean_job_functions(self):
        return ', '.join(self.cleaned_data.get('job_functions'))
    
    def clean_years_of_experience(self):
        years = self.cleaned_data.get('years_of_experience')
        if years >= 100:
            raise forms.ValidationError("Are you mad?! Only the Queen of UK has that kind of experience!")
        return years
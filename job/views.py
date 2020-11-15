from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, FormView
from django.urls import reverse, reverse_lazy

from user import mixins
from . import models
from . import forms

# Create your views here.

class EmployerJobListingListView(mixins.EmployerAccessMixin, ListView):
    template_name = 'employer/listing/job-listing-list.html'
    model = models.JobListing

    def get_queryset(self):
        self.queryset = models.JobListing.objects.filter(company__userprofile__user=self.request.user).distinct().order_by('updated_at')
        return super().get_queryset()

class EmployerJobListingCreateView(mixins.EmployerAccessMixin, FormView):
    template_name = 'employer/listing/job-listing-create.html'
    # model = models.JobListing
    # fields = ['title', 'state', 'country', 'industry', 'employment_type',
    # 'level', 'specialisation', 'qualifications', 'pay_from', 'pay_to', 'years_of_experience',
    # 'company']
    form_class = forms.JobListingCreateForm
    success_url = reverse_lazy('job:job-listing')

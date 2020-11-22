from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, FormView
from django.urls import reverse, reverse_lazy

from user import mixins
from user import models as user_models
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
    form_class = forms.JobListingCreateForm
    success_url = reverse_lazy('job:job-listing')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_logos'] = user_models.Company.objects.only('company_name', 'avatar', 'pk')
        return context
    
    def form_valid(self, form):
        # gotta set expiry with celery here
        form.save()
        return super().form_valid(form)
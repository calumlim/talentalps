from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.db import transaction

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

    def dispatch(self, request, *args, **kwargs):
        self.companies = user_models.Company.objects.filter(userprofile=self.request.user.userprofile, status=user_models.Company.STATUS_ACTIVE)
        if not self.companies:
            messages.error(request, _("You must complete at least 1 company profile to create a job listing."))
            return redirect('employer:company-list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_logos'] = self.companies.only('company_name', 'avatar', 'pk')
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['companies'] = self.companies
        return kwargs
    
    def form_valid(self, form):
        # gotta set expiry with celery here
        listing = form.save(commit=False)
        if listing.company.status == listing.company.STATUS_ACTIVE:
            listing.published = True
            listing.userprofile = self.request.user.userprofile
            listing.save()
            self.success_url = reverse('job:job-listing-description-edit', args=(listing.pk,)) + '?create=1'
        else:
            messages.error(self.request, _("The selected company has been deleted, please select another company."))
            return super().get(self.request)
        return super().form_valid(form)

class EmployerJobListingDescriptionCreateView(mixins.EmployerAccessMixin, SingleObjectMixin, FormView):
    """
    
    """
    template_name = 'employer/listing/job-listing-description-edit.html'
    form_class = forms.JobListingDescriptionCreateForm
    success_url = reverse_lazy('job:job-listing')
    model = models.JobListing

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.JobListingDescriptionCreateForm(instance=self.object)
        return context
    
    def form_valid(self, form):
        f = forms.JobListingDescriptionCreateForm(self.request.POST, instance=self.object)
        listing = f.save()
        messages.success(self.request, _(f"Description saved for - {listing.title} ({listing.company.company_name})"))
        if self.request.GET.get('create'):
            self.success_url = reverse('job:questionnaire-edit', args=(listing.pk,))
        return super().form_valid(form)
    
    def check_permission(self):
        if self.object.userprofile != self.request.user.userprofile:
            raise Http404()

class EmployerQuestionnaireCreateView(mixins.EmployerAccessMixin, SingleObjectMixin, FormView):
    """
    """
    template_name = 'employer/questionnaire/questionnaire-edit.html'
    form_class = forms.QuestionnaireFormSet
    model = models.JobListing
    success_url = reverse_lazy('job:job-listing')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_permission()
        self.questionnaire = models.Questionnaire.objects.get(joblisting=self.object)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.QuestionnaireFormSet(queryset=models.Question.objects.filter(questionnaire=self.questionnaire))
        return context
    
    def check_permission(self):
        if self.object.userprofile != self.request.user.userprofile:
            raise Http404()
    
    def form_valid(self, formset):
        instances = formset.save(commit=False)

        try:
            with transaction.atomic():
                for instance in instances:
                    if instance.question:
                        instance.questionnaire = self.questionnaire
                        instance.save()
                    else:
                        instance.delete()
                for obj in formset.deleted_objects:
                    obj.delete()
                if self.object.questionnaire.question_set.all():
                    messages.success(self.request, _(f"Questionnaire saved for - {self.object.title} ({self.object.company.company_name})"))
                    self.success_url = reverse('job:questionnaire-edit', args=(self.object.pk,))
                else:
                    messages.info(self.request, _(f"Disabled questionnaire for - {self.object.title} ({self.object.company.company_name})"))
        except:
            messages.error(self.request, _("Could not save questionnaire, please try again or contact support."))
            return super().form_invalid(formset)
        return super().form_valid(formset)
    
    def form_invalid(self, formset):
        print(formset.errors)
        return super().form_invalid(formset)
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import FormView, TemplateView, ListView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.utils.http import is_safe_url
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import transaction
from django.core import mail
from django.template.loader import render_to_string
from django.http import Http404, HttpResponseServerError, HttpResponse, JsonResponse, HttpResponseRedirect
from PIL import Image
from django.core.files import File
from django.db.models import Count, Case, When, Sum

import json
import datetime

from . import tasks
from user.forms import LogInForm
from user import mixins
from user import models as user_models
from job import models as job_models
from . import forms

User = get_user_model()

def crop_logo_header(company, form, request):
    if company.avatar:
        # Cropping company logo then scaling it to a standard size of 400x400 following the 1/1 ratio
        logo_x = form.cleaned_data.get('logo_x')
        logo_y = form.cleaned_data.get('logo_y')
        logo_w = form.cleaned_data.get('logo_w')
        logo_h = form.cleaned_data.get('logo_h')

        if (logo_x and logo_y and logo_w and logo_h):
            if logo_x < 0 or logo_y < 0 or (logo_w/logo_h != 1):
                messages.error(request, _("An error occured while trying to crop the company logo, please try again."))
                return super().get(request)

            logo = Image.open(company.avatar.file)
            cropped_logo = logo.crop((logo_x, logo_y, logo_w+logo_x, logo_h+logo_y))
            resized_logo = cropped_logo.resize((400, 400), Image.ANTIALIAS)
            resized_logo.save(company.avatar.path, quality=100)

    if company.header_image:
        # Cropping company logo then scaling it to a standard size of 800x200 following the .25/1 ratio
        header_x = form.cleaned_data.get('header_x')
        header_y = form.cleaned_data.get('header_y')
        header_w = form.cleaned_data.get('header_w')
        header_h = form.cleaned_data.get('header_h')

        if (header_x and header_y and header_w and header_h):
            if header_x < 0 or header_y < 0 or round((header_h/header_w), 2) < 0.17:
                messages.error(request, _("An error occured while trying to crop the company header, please try again."))
                return super().get(request)

            header = Image.open(company.header_image.file)
            cropped_header = header.crop((header_x, header_y, header_w+header_x, header_h+header_y))
            cropped_header.save(company.header_image.path, quality=80)

# Create your views here.
class EmployerLoginView(FormView):
    template_name = 'employer/login.html'
    form_class = LogInForm
    success_url = reverse_lazy('employer:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userprofile.is_employer:
            return redirect('employer:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.cleaned_data
        login(self.request, user)
        if not self.request.POST.get('remember_me'):
            self.request.session.set_expiry(0)

        next_url = self.request.GET.get('next')
        if is_safe_url(next_url, settings.ALLOWED_HOSTS):
            self.success_url = next_url

        if not user.userprofile.is_employer:
            self.success_url = reverse('cms:home')
        return super().form_valid(form)

class EmployerDashboardView(mixins.EmployerAccessMixin, TemplateView):
    template_name = 'employer/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_traffic'] = job_models.JobListing.objects.filter(userprofile=self.request.user.userprofile).aggregate(total=Sum('views'))
        context['job_applications_count'] = job_models.JobApplication.objects.filter(joblisting__userprofile=self.request.user.userprofile).count()
        return context
    

class EmployerForgotPasswordView(FormView):
    template_name = 'employer/forgot-password.html' 
    form_class = forms.ForgotPasswordForm
    success_url = reverse_lazy('employer:forgot-password-email-sent')

    def form_valid(self, form):
        try:
            user = User.objects.get(email=form.cleaned_data.get('email'))
            self.send_email(user)
        except User.DoesNotExist:
            return super().form_valid(form)
        return super().form_valid(form)

    def send_email(self, user):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        url = self.request.build_absolute_uri(reverse('employer:reset-password', args=(user.pk, token,)))

        context = {
            'user': user,
            'activation_url': url,
        }

        message = render_to_string("emails/reset-password-email.txt", context=context, request=self.request)
        html_message = render_to_string("emails/reset-password-email.html", context=context, request=self.request)

        subject = 'Reset your password - TalentAlps'
        from_email = settings.DEFAULT_FROM_EMAIL
        to = user.email

        mail.send_mail(subject, message, from_email, [to], html_message=html_message)

class EmployerForgotPasswordEmailSentView(TemplateView):
    template_name = 'employer/forgot-password-email-sent.html'

class EmployerResetPasswordView(SingleObjectMixin, FormView):
    template_name = 'employer/reset-password.html'
    form_class = forms.ResetPasswordForm
    model = User
    success_url = reverse_lazy('employer:reset-password-success')

    def dispatch(self, request, *args, **kwargs):
        token = self.kwargs.get('token')
        self.object = self.get_object()
        token_generator = PasswordResetTokenGenerator()

        self.valid = False

        if token_generator.check_token(self.object, token):
            self.valid = True
        else:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        if not self.valid:
            messages.error(self.request, _("Something went wrong, please try again."))
            return super().form_invalid(form)
            
        password = form.cleaned_data.get('password')
        user = self.object
        try:
            with transaction.atomic():
                if user.has_usable_password():
                    user.set_password(password)
                    user.save()
                    self.send_email(user)
                else:
                    messages.error(self.request, _("Something went wrong, please try again, log in with other method(s), or contact support."))
                    return super().form_invalid(form)
        except:
            messages.error(self.request, _("Something went wrong, please try again."))
            return super().form_invalid(form)

        messages.success(self.request, _("Password has been reset, please login using your new password."))
        return super().form_valid(form)

    def send_email(self, user):
        context = {
            'user': user,
            'activation_url': self.request.build_absolute_uri(reverse('employer:login'))
        }

        message = render_to_string("emails/reset-password-success.txt", context=context, request=self.request)
        html_message = render_to_string("emails/reset-password-success.html", context=context, request=self.request)

        subject = "You've just reset your password! - TalentAlps"
        from_email = settings.DEFAULT_FROM_EMAIL
        to = user.email

        mail.send_mail(subject, message, from_email, [to], html_message=html_message)

class EmployerResetPasswordSuccess(TemplateView):
    template_name = 'employer/reset-password-success.html'

class EmployerJobApplicationsPendingListView(TemplateView):
    template_name = 'employer/job-applications-pending-list.html'

class EmployerJobApplicationReviewedListView(TemplateView):
    template_name = 'employer/job-applications-reviewed-list.html'

class EmployerCompanyListView(mixins.EmployerAccessMixin, ListView):
    template_name = 'employer/company/company-list.html'

    def get_queryset(self):
        self.queryset = user_models.Company.objects.filter(userprofile=self.request.user.userprofile, status=user_models.Company.STATUS_ACTIVE).annotate(
            listing_count=Count(Case(When(joblisting__expired=False, then=1)))).annotate(
                total_views=Sum('joblisting__views')).order_by('created_at')
        return super().get_queryset()

class EmployerCompanyUpdateView(mixins.EmployerAccessMixin, SingleObjectMixin, FormView):
    template_name = 'employer/company/company-update.html'
    model = user_models.Company
    success_url = reverse_lazy('employer:company-list')
    form_class = forms.EmployerCompanyUpdateForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.EmployerCompanyUpdateForm(instance=self.object)
        return context
    
    def form_valid(self, form):
        f = forms.EmployerCompanyUpdateForm(self.request.POST, files=self.request.FILES, instance=self.object)
        company = f.save(commit=False)
        if company.industry != 'Other':
            company.other_industry = None
        
        try:
            with transaction.atomic():
                company.save()
                crop_logo_header(company, form, self.request)
                messages.success(self.request, _(f"Company - {company.company_name} updated successfully!"))
        except:
            messages.error(self.request, _("An error occured while trying to save this company's profile, please try again or contact support."))
            return super().get(self.request)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, _(f"{form.errors}"))
        return self.get(self.request)


class EmployerCompanyCreateView(mixins.EmployerAccessMixin, FormView):
    template_name = 'employer/company/company-create.html'
    form_class = forms.CompanyDetailsCreateForm

    def form_valid(self, form):
        company = form.save(commit=False)
        company.userprofile = self.request.user.userprofile
        if company.industry != 'Other':
            company.other_industry = None

        try:
            with transaction.atomic():
                company.save()
                crop_logo_header(company, form, self.request)
            self.success_url = reverse('employer:company-description-location-create', args=(company.pk,))
        except:
            messages.error(self.request, _("An error occured while trying to create your company's profile, please try again or contact support."))
            return super().get(self.request)
        return super().form_valid(form)

class EmployerCompanyDescriptionLocationCreateView(mixins.EmployerAccessMixin, FormView):
    template_name = 'employer/company/company-description-location-create.html'
    form_class = forms.CompanyCreateDescriptionLocationForm

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(user_models.Company, pk=self.kwargs.get('pk'))
        if self.object.description or self.object.country or self.object.userprofile != request.user.userprofile:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        f = forms.CompanyCreateDescriptionLocationForm(self.request.POST, instance=self.object)
        company = f.save(commit=False)
        company.status = company.STATUS_ACTIVE
        company.save()

        messages.success(self.request, _(f"Company profile - {company.company_name} created!"))
        self.success_url = f'{reverse("employer:company-image-upload", args=(company.pk,))}?create=1'
        return super().form_valid(form)

class EmployerCompanyImageUploadView(mixins.EmployerAccessMixin, SingleObjectMixin, TemplateView):
    model = user_models.Company
    template_name = 'employer/company/company-image-upload.html'

    def check_permission(self):
        if self.object.userprofile != self.request.user.userprofile or self.object.status != self.object.STATUS_ACTIVE:
            raise Http404()
        return True

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.check_permission()
        if 'upload_image' in request.POST:
            f = forms.CompanyImageUploadForm(request.POST, files=request.FILES)
            if f.is_valid():
                f = f.save(commit=False)
                f.company = self.object
                image = Image.open(f.image.file)
                resized_image = image.resize((1280, 720), Image.ANTIALIAS)
                resized_image.save(f.image.path)
                f.set_next_order()
                f.save()
                return JsonResponse({
                    'pk': f.pk,
                    'url': f.image.url,
                    'order': f.order,
                })
            else:
                return HttpResponseServerError()

        elif 'arrange_image' in request.POST:
            status = tasks.update_company_image_order.delay(request.POST.get('order'), self.object.pk)
            if status == False:
                return HttpResponseServerError()
        
        elif 'delete_image' in request.POST:
            status = tasks.delete_company_image.delay(request.POST.get('id'), self.object.pk)
            if status == False:
                return HttpResponseServerError()
            else:
                messages.success(request, _("Image deleted successfully!"))
        return HttpResponse()


class EmployerDeleteView(mixins.EmployerAccessMixin, DeleteView):
    model = user_models.Company
    template_name = 'employer/company/company-delete.html'
    success_url = reverse_lazy('employer:company-list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.check_permission()
        self.object.status = self.object.STATUS_INACTIVE
        self.object.save()
        messages.error(request, _(f"{self.object.company_name} has been deleted."))
        return redirect(self.success_url)
    
    def check_permission(self):
        if self.object.userprofile != self.request.user.userprofile or self.object.status != self.object.STATUS_ACTIVE:
            raise Http404()
        return True
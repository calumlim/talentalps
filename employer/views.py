from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView, ListView
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
from django.http import Http404
from PIL import Image
from django.core.files import File
from django.db.models import Count, Case, When, Sum

from user.forms import LogInForm
from user import mixins
from user import models as user_models
from . import forms

User = get_user_model()

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
        self.queryset = user_models.Company.objects.filter(userprofile=self.request.user.userprofile).annotate(
            listing_count=Count(Case(When(joblisting__expired=False, then=1)))).annotate(
                total_views=Sum('joblisting__views'))
        return super().get_queryset()

class EmployerCompanyCreateView(mixins.EmployerAccessMixin, FormView):
    template_name = 'employer/company/company-create.html'
    form_class = forms.CompanyCreateForm
    success_url = reverse_lazy('employer:company-create')

    def form_valid(self, form):
        company = form.save(commit=False)
        company.userprofile = self.request.user.userprofile

        try:
            with transaction.atomic():
                company.save()
                if company.avatar:
                    # Cropping company logo then scaling it to a standard size of 400x400 following the 1/1 ratio
                    logo_x = form.cleaned_data.get('logo_x')
                    logo_y = form.cleaned_data.get('logo_y')
                    logo_w = form.cleaned_data.get('logo_w')
                    logo_h = form.cleaned_data.get('logo_h')
                    
                    if logo_x < 0 or logo_y < 0 or (logo_w/logo_h != 1):
                        messages.error(self.request, _("An error occured while trying to crop the company logo, please try again."))
                        return super().get(self.request)

                    logo = Image.open(company.avatar.file)
                    cropped_logo = logo.crop((logo_x, logo_y, logo_w+logo_x, logo_h+logo_y))
                    resized_logo = cropped_logo.resize((400, 400), Image.ANTIALIAS)
                    resized_logo.save(company.avatar.path)

                if company.header_image:
                    # Cropping company logo then scaling it to a standard size of 800x200 following the .25/1 ratio
                    header_x = form.cleaned_data.get('header_x')
                    header_y = form.cleaned_data.get('header_y')
                    header_w = form.cleaned_data.get('header_w')
                    header_h = form.cleaned_data.get('header_h')
                    if header_x < 0 or header_y < 0 or round((header_h/header_w), 2) < 0.25:
                        messages.error(self.request, _("An error occured while trying to crop the company logo, please try again."))
                        return super().get(self.request)

                    header = Image.open(company.header_image.file)
                    cropped_header = header.crop((header_x, header_y, header_w+header_x, header_h+header_y))
                    resized_header = cropped_header.resize((800, 200), Image.ANTIALIAS)
                    resized_header.save(company.header_image.path)
        except:
            messages.error(self.request, _("An error occured while trying to create your company's profile, please try again or contact support."))
            return super().get(self.request)
        return super().form_valid(form)
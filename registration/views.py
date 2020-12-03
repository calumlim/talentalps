from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings

from user.models import UserProfile, Candidate
from . import forms
from user.forms import ResetPasswordEmailForm

User = get_user_model()

def send_verification_email(user, url, request):
    context = {
        'user': user,
        'activation_url': url,
    }

    message = render_to_string("emails/email-verification.txt", context=context, request=request)
    html_message = render_to_string("emails/email-verification.html", context=context, request=request)

    subject = 'Verify your account! - TalentAlps'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = user.email

    mail.send_mail(subject, message, from_email, [to], html_message=html_message)

# Create your views here.
class CandidateRegisterView(FormView):
    template_name = 'registration/candidate-registration.html'
    form_class = forms.UserProfileForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['candidate_form'] = forms.CandidateRegisterForm()
        return context
    
    def form_valid(self, form):
        candidate_form = forms.CandidateRegisterForm(self.request.POST)
        if candidate_form.is_valid():
            # Create User, UserProfile, Candidate models
            try:
                with transaction.atomic():
                    user = User.objects.create(
                        username=form.cleaned_data.get('username'),
                        email=form.cleaned_data.get('email'),
                        first_name=form.cleaned_data.get('name')
                    )
                    user.set_password(form.cleaned_data.get('password'))
                    user.save()

                    userprofile = UserProfile.objects.create(
                        name=form.cleaned_data.get('name'),
                        contact=form.cleaned_data.get('contact'),
                        state=form.cleaned_data.get('state'),
                        country=form.cleaned_data.get('country'),
                        user=user
                    )

                    candidate = candidate_form.save(commit=False)
                    candidate.state = form.cleaned_data.get('state')
                    candidate.nationality = form.cleaned_data.get('country')
                    candidate.userprofile = userprofile
                    candidate.save()

                    token_generator = PasswordResetTokenGenerator()
                    token = token_generator.make_token(user)
                    url = self.request.build_absolute_uri(reverse('registration:email-verify', args=(user.pk, token)))

                    send_verification_email(user, url, self.request)
                    messages.info(self.request, _(f"A verification email has been sent to - {user.email}, you must verify your account before you can log in."))
                    return super().form_valid(form)
            except:
                messages.error(self.request, _("Something went wrong, please try again."))
                return super().get(self.request)
        else:
            return super().form_invalid(candidate_form)
    

class EmployerRegisterView(FormView):
    template_name = 'registration/employer-registration.html'
    form_class = forms.UserProfileForm
    success_url = reverse_lazy('registration:employer-register-success')

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = User.objects.create(
                    username=form.cleaned_data.get('email'),
                    email=form.cleaned_data.get('email'),
                    first_name=form.cleaned_data.get('name'),
                )
                user.set_password(form.cleaned_data.get('password'))
                user.save()
                userprofile = user.userprofile
                userprofile.is_employer = True
                userprofile.receive_updates = form.cleaned_data.get('receive_updates')
                userprofile.save()

                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                url = self.request.build_absolute_uri(reverse('registration:email-verify', args=(user.pk, token)))

                send_verification_email(user, url, self.request)
                messages.info(self.request, _(f"A verification email has been sent to - {user.email}, you must verify your account before you can log in."))
                return super().form_valid(form)
        except:
            messages.error(self.request, _("Something went wrong, please try again."))
            return super().get(self.request)

class EmployerRegistrationSuccessView(TemplateView):
    template_name = 'registration/employer-registration-success.html'

class EmployerResendVerificationEmailView(TemplateView):
    template_name = 'registration/employer-resend-verification-email.html'


class UserEmailVerificationView(TemplateView):
    template_name = 'registration/user-email-verification.html'
    
    def get(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=self.kwargs.get('pk'))
        token_generator = PasswordResetTokenGenerator()
        url_token = self.kwargs.get('token')
        
        self.valid = False
        self.verified = False

        if token_generator.check_token(self.user, url_token):
            self.valid = True
            if self.user.userprofile.verified:
                self.verified = True
            self.user.userprofile.verified = True
            self.user.userprofile.save()
        return super().get(request, *args, **kwargs)

class ResendVerificationEmail(FormView):
    template_name = 'registration/resend-verification.html'
    form_class = ResetPasswordEmailForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.info(self.request, _(f"Verification email has been sent to - {form.cleaned_data.get('email')}, please check your inbox."))
        try:
            user = User.objects.get(email=form.cleaned_data.get('email'))
            if not user.userprofile.verified:
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                url = self.request.build_absolute_uri(reverse('registration:email-verify', args=(user.pk, token)))
                send_verification_email(user, url, self.request)
        except User.DoesNotExist:
            return super().form_valid(form)
        return super().form_valid(form)

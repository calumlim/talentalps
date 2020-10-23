from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.db import transaction

from django.core import mail
from django.template.loader import render_to_string

from . import forms

# Create your views here.
class LogInView(FormView):
    template_name = 'user/login.html'
    form_class = forms.LogInForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
        if user is not None:
            login(self.request, user)
        else:
            messages.error(self.request, _("Username or password is incorrect."))
            return super().get(self.request)
        return super().form_valid(form)

def LogOut(request):
    logout(request)

    messages.info(request, _("You have logged out."))

    return redirect(reverse_lazy('login'))

class ResetPasswordEmailView(FormView):
    template_name = 'user/reset-password-email.html'
    form_class = forms.ResetPasswordEmailForm
    success_url = reverse_lazy('user:reset-password-email-sent')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            url = self.request.build_absolute_uri(reverse('user:reset-password-form', args=(user.pk, token)))

            logout(self.request)
            self.request.session['email'] = user.email
            self.send_email(user, url)
        except User.DoesNotExist:
            self.request.session['email'] = email
            pass
        return super().form_valid(form)
    
    def send_email(self, user, url):
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

class ResetPasswordEmailSentView(TemplateView):
    template_name = 'user/reset-password-email-sent.html'

class ResetPasswordView(FormView):
    template_name = 'user/reset-password-form.html'
    form_class = forms.ResetPasswordForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=self.kwargs.get('pk'))
        token = self.kwargs.get('token')
        token_generator = PasswordResetTokenGenerator()

        self.valid = False
        self.valid_password = False

        if token_generator.check_token(self.user, token):
            self.valid = True
            if self.user.has_usable_password():
                self.valid_password = True
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if not self.valid:
            messages.error(self.request, _("Something went wrong, please try again."))
            return super().form_invalid(form)
            
        password = form.cleaned_data.get('password')
        user = self.user
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

        messages.info(self.request, _("Password has been reset, please login using your new password."))
        return super().form_valid(form)

    def send_email(self, user):
        context = {
            'user': user,
            'activation_url': self.request.build_absolute_uri(reverse('login'))
        }

        message = render_to_string("emails/reset-password-success.txt", context=context, request=self.request)
        html_message = render_to_string("emails/reset-password-success.html", context=context, request=self.request)

        subject = "You've just reset your password! - TalentAlps"
        from_email = settings.DEFAULT_FROM_EMAIL
        to = user.email

        mail.send_mail(subject, message, from_email, [to], html_message=html_message)
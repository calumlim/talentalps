from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from user.forms import LogInForm
from user import mixins

# Create your views here.
class EmployerLoginView(FormView):
    template_name = 'employer/login.html'
    form_class = LogInForm
    success_url = reverse_lazy('employer:login')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))

        if user is not None:
            if user.userprofile.verified:
                login(self.request, user)
                return super().form_valid(form)
            else:
                messages.info(self.request, _("Please verify your account before you log in."))
                return super().get(self.request)
        else:
            messages.error(self.request, _("Username or password is incorrect."))
        return super().get(self.request)

class EmployerDashboardView(mixins.EmployerAccessMixin, TemplateView):
    template_name = 'employer/dashboard.html'
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from user.forms import LogInForm
# Create your views here.
class EmployerLoginView(FormView):
    template_name = 'employer/login.html'
    form_class = LogInForm
    success_url = reverse_lazy('employer:login')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))

        if user is not None:
            login(self.request, user)
            if user.userprofile.is_employer:
                return super().form_valid(form)
            else:
                return redirect('login')

        else:
            messages.error(self.request, _("Username or password is incorrect."))
        return super().form_valid(form)

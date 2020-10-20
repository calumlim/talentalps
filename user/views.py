from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect

from . import forms

# Create your views here.
class LogInView(FormView):
    template_name = 'user/login.html'
    form_class = forms.LogInForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
        if user is not None:
            login(self.request, user)
        else:
            messages.error(self.request, _("Login credentials were incorrect."))
        return super().form_valid(form)

def LogOut(request):
    logout(request)

    messages.info(request, _("You have logged out."))

    return redirect(reverse_lazy('user:login'))


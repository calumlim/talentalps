from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy

# Create your views here.
class HomeView(TemplateView):
    template_name = 'cms/home.html'

class FAQView(TemplateView):
    template_name = 'cms/faq.html'

class TermsAndConditionView(TemplateView):
    template_name = 'cms/tnc.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'cms/pee-pee.html'

class ContactView(TemplateView):
    template_name = 'cms/contact.html'
    
class SupportView(TemplateView):
    template_name = 'cms/support.html'

def LoginRedirect(request):
    if (request.user.is_authenticated and request.user.is_employer):
        return redirect('employer:dashboard')
    elif (request.user.is_authenticated and not request.user.is_employer):
        return redirect('cms:home')
    return redirect('cms:home')

class ErrorView(TemplateView):
    template_name = '404.html'
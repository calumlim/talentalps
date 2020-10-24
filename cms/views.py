from django.shortcuts import render
from django.views.generic import TemplateView

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
    
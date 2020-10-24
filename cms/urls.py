from django.urls import path
from django.urls import include

from . import views

app_name = 'cms'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('redirect/', views.LoginRedirect, name='redirect'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('tnc/', views.TermsAndConditionView.as_view(), name='t&c'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('support/', views.SupportView.as_view(), name='support'),
    
]
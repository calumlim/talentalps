from django.urls import path
from django.urls import include

from . import views

app_name = 'registration'
urlpatterns = [
    path('', views.CandidateRegisterView.as_view(), name='candidate-register'),
    path('employer/', views.EmployerRegisterView.as_view(), name='employer-register'),
    path('email-verification/resend/', views.ResendVerificationEmail.as_view(), name='resend-email-verification'),
    path('email-verification/<int:pk>/<str:token>/', views.UserEmailVerificationView.as_view(), name='email-verify'),
    path('employer/success/', views.EmployerRegistrationSuccessView.as_view(), name='employer-register-success'),
    path('employer/email-verification/resend/', views.EmployerResendVerificationEmailView.as_view(), name='employer-resend-email-verification'),
]
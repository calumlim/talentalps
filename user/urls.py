from django.urls import path
from django.urls import include

from . import views

app_name = 'user'



urlpatterns = [
    path('logout/', views.LogOut, name='logout'),
    path('reset-password/', views.ResetPasswordEmailView.as_view(), name='reset-password-email'),
    path('reset-password/<int:pk>/<str:token>/', views.ResetPasswordView.as_view(), name='reset-password-form'),
    path('reset-password/done/', views.ResetPasswordEmailSentView.as_view(), name='reset-password-email-sent'),
]

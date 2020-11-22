from django.urls import path, include

from . import views

app_name = 'employer'

forgot_password_urlpatterns = [
    path('', views.EmployerForgotPasswordView.as_view(), name='forgot-password'),
    path('email-sent/', views.EmployerForgotPasswordEmailSentView.as_view(), name='forgot-password-email-sent'),
]

reset_password_urlpatterns = [
    path('<int:pk>/<str:token>/', views.EmployerResetPasswordView.as_view(), name='reset-password'),
    path('success/', views.EmployerResetPasswordSuccess.as_view(), name='reset-password-success'),
]

job_applications_urlpatterns = [
    path('pending/', views.EmployerJobApplicationsPendingListView.as_view(), name='job-application-pending'),
    path('reviewed/', views.EmployerJobApplicationReviewedListView.as_view(), name='job-application-reviewed'),
]

company_urlpatterns = [
    path('', views.EmployerCompanyListView.as_view(), name='company-list'),
    path('create/', views.EmployerCompanyCreateView.as_view(), name='company-create'),
]

urlpatterns = [
    path('login/', views.EmployerLoginView.as_view(), name='login'),
    path('dashboard/', views.EmployerDashboardView.as_view(), name='dashboard'),
    path('forgot-password/', include(forgot_password_urlpatterns)),
    path('reset-password/', include(reset_password_urlpatterns)),
    path('job-applications/', include(job_applications_urlpatterns)),
    path('company/', include(company_urlpatterns)),
]
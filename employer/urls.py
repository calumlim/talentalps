from django.urls import path
from django.urls import include

from . import views

app_name = 'employer'
urlpatterns = [
    path('login/', views.EmployerLoginView.as_view(), name='login'),
]
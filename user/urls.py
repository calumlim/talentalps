from django.urls import path
from django.urls import include

from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogOut, name='logout'),
    # path('logout/', views.LogOutView.as_view(), name='logout'),
    # path('signup/', views.SignUpView.as_view(), name='signup'),
    # path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),

]

from django.urls import path
from django.urls import include

from . import views

app_name = 'job'

job_listing_urlpatterns = [
    path('', views.EmployerJobListingListView.as_view(), name='job-listing'),
    path('create/', views.EmployerJobListingCreateView.as_view(), name='job-listing-create'),
]

urlpatterns = [
    path('employer/job-listing/', include(job_listing_urlpatterns)),
]
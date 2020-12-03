from django.urls import path
from django.urls import include

from . import views

app_name = 'job'

job_listing_urlpatterns = [
    path('', views.EmployerJobListingListView.as_view(), name='job-listing'),
    path('create/', views.EmployerJobListingCreateView.as_view(), name='job-listing-create'),
    path('edit/description/<str:pk>/', views.EmployerJobListingDescriptionCreateView.as_view(), name='job-listing-description-edit'),
]

questionnaire_urlpatterns =  [
    path('edit/<str:pk>/', views.EmployerQuestionnaireCreateView.as_view(), name='questionnaire-edit'),
]

urlpatterns = [
    path('employer/listing/', include(job_listing_urlpatterns)),
    path('employer/questionnaire/', include(questionnaire_urlpatterns)),
]
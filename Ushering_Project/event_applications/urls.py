from django.urls import path
from event_applications import views as app_views


urlpatterns = [
    path('apply/<uuid:event_id>/', app_views.apply_for_event, name='usherly-apply'),
    path('applicants/<uuid:event_id>/', app_views.view_applicants, name='usherly-applicants'),
    path('<uuid:event_id>/applicants/<uuid:application_id>/', app_views.applicant_detail, name='usherly-applicant-detail'),
    path('<uuid:application_id>/status/', app_views.usherly_accept_reject_view, name='usherly-accept-reject'),
    
]
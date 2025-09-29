from django.urls import path
from .views import EventListView, EventDetailView, EventDeleteView, EventUpdateView
from . import views as event_views



urlpatterns = [
    path('', EventListView.as_view(), name='usherly-events'),
    path('<uuid:event_id>/', EventDetailView.as_view(), name='usherly-detail'),
    path('<uuid:event_id>/edit-event/', EventUpdateView.as_view(), name='usherly-event-edit'),
    path('<uuid:event_id>/delete', EventDeleteView.as_view(), name='usherly-event-delete'),
    
]

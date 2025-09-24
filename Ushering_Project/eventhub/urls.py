from django.urls import path
from .views import EventListView, EventDetailView



urlpatterns = [
    path('', EventListView.as_view(), name='usherly-events'),
    path('<str:event_id>/', EventDetailView.as_view(), name='usherly-detail'),
    
]

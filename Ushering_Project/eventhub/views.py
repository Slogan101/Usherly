from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Events
from users.models import HostProfile
from .forms import CreateEventForm
# Create your views here.



class EventListView(ListView):
    model = Events
    template_name = 'eventhub/events_list.html'
    context_object_name = 'events'
    ordering = '-created_at'

    def get_queryset(self):
        queryset = Events.objects.all()
        state = self.request.GET.get('state')
        event_type = self.request.GET.get('event_type')
        pay = self.request.GET.get('pay')

        if state:
            queryset = queryset.filter(state=state)
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        if pay:
            queryset = queryset.filter(pay_amount__gte=pay)

        return queryset
    

class EventDetailView(DetailView):
    model = Events
    template_name = 'eventhub/event_details.html'
    context_object_name ='event'
    pk_url_kwarg = 'event_id'


    

    

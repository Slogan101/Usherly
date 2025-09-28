from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Events
from users.models import UsherProfile
from event_applications.models import Application
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


    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       user = self.request.user
       event = self.get_object()
       application = None
       if user.is_authenticated:
           try:
               usher_profile = user.usher_profile
               application = Application.objects.filter(event=event, usher=usher_profile).first()
           except UsherProfile.DoesNotExist:
               pass  # user is not an usher
       context['application'] = application  # will be None or an Application instance
       return context


    

    

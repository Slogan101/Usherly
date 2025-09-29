from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from .models import Events
from django.urls import reverse_lazy
from users.models import UsherProfile
from event_applications.models import Application
from .forms import EventUpdateForm
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

# def event_edit(request, event_id):
#     user = request.user
#     profile = user.host_profile
#     event = get_object_or_404(Events, id=event_id)

#     if event.host != profile:
#         return HttpResponseForbidden("You are not allowed to edit this event.")

#     if request.method == 'POST':
#         form = EventUpdateForm(request.POST, request.FILES, instance=event)
#         if form.is_valid():
#             form.save()
#             return redirect('usherly-host')
#         else:
#             print(form.errors)
#     else:
#         form = EventUpdateForm(instance=event)
#     return render(request, 'eventhub/event_edit.html', {'form': form, 'event': event})




class EventUpdateView(UpdateView):
    model = Events
    fields = ['title', 'event_image', 'event_type', 'state', 'event_duration', 'event_description', 'pay_amount', 'event_date']
    template_name = 'eventhub/event_edit.html'
    pk_url_kwarg = 'event_id'
    context_object_name = 'event'
    success_url = reverse_lazy('usherly-host')

    def form_valid(self, form):
        form.instance.host = self.request.user.host_profile
        return super().form_valid(form)
    
    def test_func(self):
        event = self.get_object()
        return self.request.user == event.host



class EventDeleteView(DeleteView):
    model = Events
    success_url = reverse_lazy('usherly-host')
    pk_url_kwarg = 'event_id'
    context_object_name = 'event'

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.host

    

from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Events, Ticket
from django.urls import reverse_lazy
from users.models import UsherProfile
from event_applications.models import Application
from .forms import EventUpdateForm
from decimal import Decimal
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




class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Events
    form_class = EventUpdateForm
    template_name = 'eventhub/event_edit.html'
    pk_url_kwarg = 'event_id'
    context_object_name = 'event'
    success_url = reverse_lazy('usherly-host')
    
    def test_func(self):
        event = self.get_object()
        return self.request.user.host_profile == event.host
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = self.object.tickets.all()  # Assuming related_name='tickets'
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            form.instance.host = self.request.user.host_profile
            form.save()

            # Handle tickets manually
            ticket_count = int(request.POST.get('ticket_count', 0))
            for i in range(1, ticket_count + 1):
                ticket_id = request.POST.get(f'ticket_id_{i}')
                ticket_type = request.POST.get(f'ticket_type_{i}')
                ticket_price = request.POST.get(f'ticket_price_{i}')
                ticket_quantity = request.POST.get(f'ticket_quantity_{i}')

                if ticket_id:
                    try:
                        ticket = Ticket.objects.get(id=ticket_id, event=self.object)

                        #Convert to correct types
                        ticket.ticket_type = ticket_type
                        ticket.price = Decimal(ticket_price)  # Convert to Decimal
                        ticket.total_quantity = int(ticket_quantity)
                        ticket.save()
                    except Ticket.DoesNotExist:
                        pass  # optionally log or raise

            return redirect(self.success_url)

        return self.form_invalid(form)



class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Events
    success_url = reverse_lazy('usherly-host')
    pk_url_kwarg = 'event_id'
    context_object_name = 'event'

    def test_func(self):
        event = self.get_object()
        return self.request.user.host_profile == event.host

    
# VIEW FOR TICKETING

class TicketView(DetailView):
    model = Events
    template_name = 'eventhub/tickets.html'
    context_object_name = 'event'
    pk_url_kwarg = 'event_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the event object
        event = self.get_object()
        # Add related tickets to the context
        context['tickets'] = event.tickets.all()
        return context



def ticket_purchase(request):
    return render(request, 'eventhub/ticket-purchase.html')


class TicketPurchaseView(View):
    def post(self, request, event_id, ticket_id):
        event = get_object_or_404(Events, id=event_id)
        ticket = get_object_or_404(Ticket, id=ticket_id, event__id=event_id)
        quantity = int(request.POST.get('quantity', 1))
        

        # Optional: Validate quantity <= available_quantity
        if quantity > ticket.available_quantity:
            return HttpResponseBadRequest("Not enough tickets available.")
        
        base_price = ticket.price * quantity
        tax_rate = Decimal('0.075')  # 7.5% tax
        service_fee = Decimal('500.00')  # Flat fee

        tax_amount = base_price * tax_rate
        total_price = base_price + tax_amount + service_fee


        # Pass to checkout template
        return render(request, 'eventhub/ticket_purchase.html', {
            'ticket': ticket,
            'event': event,
            'quantity': quantity,
            'base_price': base_price,
            'tax_amount': tax_amount,
            'service_fee': service_fee,
            'total_price': total_price,
        })

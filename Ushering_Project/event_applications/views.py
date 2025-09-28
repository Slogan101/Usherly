from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib import messages
from eventhub.models import Events
from event_applications.models import Application
from users.models import HostProfile

# Create your views here.




def apply_for_event(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    usher_profile = request.user.usher_profile  

    # Check if application already exists
    existing_app = Application.objects.filter(usher=usher_profile, event=event).first()
    if existing_app:
        messages.warning(request, "You have already applied for this event.")
        return redirect('usherly-detail', event_id=event.id)

    # Create new application
    Application.objects.create(usher=usher_profile, event=event)
    messages.success(request, "Application submitted successfully!")
    return redirect('usherly-detail', event_id=event.id)


def view_applicants(request, event_id):
    host_profile = get_object_or_404(HostProfile, user=request.user)
    event = get_object_or_404(Events, id=event_id, host=host_profile)

    applicants = event.applications.select_related('usher').all()

    return render(request, 'event_applications/applicant_list.html', {'applicants':applicants, 'event':event})


def applicant_detail(request, event_id, application_id):
    # Get the host profile
    host_profile = get_object_or_404(HostProfile, user=request.user)

    # Ensure the event exists and belongs to the host
    event = get_object_or_404(Events, id=event_id, host=host_profile)

    # Ensure the application is tied to the event
    application = get_object_or_404(Application, id=application_id, event=event)

    return render(request, 'event_applications/applicant_detail.html', {'application': application,'event': event,})



def usherly_accept_reject_view(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'accept':
            application.update_status('accepted')
        elif action == 'reject':
            application.update_status('rejected')

        # 🛠 FIX: Redirect with BOTH event_id and application_id
        return redirect('usherly-applicant-detail', event_id=application.event.id, application_id=application.id)

    # Fallback
    return redirect('usherly-applicant-detail', event_id=application.event.id, application_id=application.id)


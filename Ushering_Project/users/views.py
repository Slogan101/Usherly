from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, LoginForm, UsherUpdateForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import UsherProfile, HostProfile
from eventhub.forms import CreateEventForm
from eventhub.models import Events
from django.utils import timezone
from event_applications.models import Application
from django.db.models import Count

# Create your views here.



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usherly-login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def usher_profile(request):
    usher = request.user.usher_profile
    applications = Application.objects.filter(usher=usher)

    return render(request, 'users/usher_dashboard.html', {'applications': applications})





def host_profile(request):
    user = request.user
    profile = user.host_profile

    host_events = Events.objects.filter(host=profile).annotate(applicant_count=Count('applications'))

    if request.method == "POST":
        form = CreateEventForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['event_date'] < timezone.now():
                form.add_error('event_date', 'Date cannot be in the past.')
            else:   
                event = form.save(commit=False)
                event.host =profile
                event.save()
                return redirect('usherly-host')
        else:
            print(form.errors) 
    else:
        form = CreateEventForm(instance=profile)
    return render(request, 'users/host_dashboard.html', {'form': form, 'events': host_events, 'now':timezone.now()})




class RoleBasedLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = LoginForm

    def get_success_url(self):
        user = self.request.user
        if user.user_type == 'usher':
            return reverse_lazy('usherly-usher')  
        elif user.user_type == 'host':
            return reverse_lazy('usherly-host')
        return reverse_lazy('usherly-home')



def edit_profile(request):
    user = request.user
    profile = user.usher_profile

    if request.method == 'POST':
        form = UsherUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('usherly-usher')
        else:
            print(form.errors)  
    else:
        form = UsherUpdateForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})


def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile_picture = request.FILES['profile_picture']

        try:
            profile = UsherProfile.objects.get(user=request.user)
            profile.profile_picture = profile_picture
            profile.save()
            return redirect('usherly-usher')
        except UsherProfile.DoesNotExist:
            try:
                # Try HostProfile next
                profile = HostProfile.objects.get(user=request.user)
                profile.profile_picture = profile_picture
                profile.save()
                return redirect('usherly-host')
            except HostProfile.DoesNotExist:
                return redirect('usherly-host')

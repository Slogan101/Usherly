from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, LoginForm, UsherUpdateForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import UsherProfile

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
    return render(request, 'users/usher_dashboard.html')

def host_profile(request):
    return render(request, 'users/host_dashboard.html')

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


# def edit_profile(request):
#     profile = get_object_or_404(UsherProfile, user=request.user)
#     if request.method == 'POST':
#         form = UsherUpdateForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Profile Updated")
#             return redirect('usherly-usher')
#     else:
#         form = UsherUpdateForm(instance=profile)
#     return render(request, 'users/edit_profile.html', {'form':form})

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
        profile = get_object_or_404(UsherProfile, user=request.user)
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
    return redirect('usherly-usher')
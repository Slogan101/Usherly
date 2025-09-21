from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

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
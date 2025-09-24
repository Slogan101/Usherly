from django.shortcuts import render
from eventhub.models import Events

# Create your views here.


def home(request):
    event = Events.objects.all()[:6]

    return render(request, 'core/home.html', {'events': event})


def about(request):
    return render(request, 'core/about.html', {'title':'About'})

def contact(request):
    return render(request, 'core/contact.html', {'title':'Contact'})

def subscription(request):
    return render(request, 'core/subscription.html', {'title':'subscribe'})
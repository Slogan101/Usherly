from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html', {'title':'About'})

def contact(request):
    return render(request, 'core/contact.html', {'title':'Contact'})

def subscription(request):
    return render(request, 'core/subscription.html', {'title':'subscribe'})
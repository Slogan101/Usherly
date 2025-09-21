from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='usherly-home'),
    path('about/', views.about, name='usherly-about'),
    path('contact/', views.contact, name='usherly-contact'),
    path('subscribe/', views.subscription, name='usherly-subscribe'),
]
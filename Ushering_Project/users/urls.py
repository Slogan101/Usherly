from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('register', user_views.register, name='usherly-register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=LoginForm), name='usherly-login'),
]
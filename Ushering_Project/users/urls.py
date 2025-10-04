from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from .views import RoleBasedLoginView, EditProfileView


urlpatterns = [
    path('register', user_views.register, name='usherly-register'),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=LoginForm), name='usherly-login'),
    path('login/', RoleBasedLoginView.as_view(), name='usherly-login'),
    path('logout/', auth_views.LogoutView.as_view(), name='usherly-logout'),
    path('dashboard/usher/', user_views.usher_profile, name='usherly-usher'),
    path('dashboard/host/', user_views.host_profile, name='usherly-host'),
    path('edit-profile/', EditProfileView.as_view(), name='usherly-edit'),
    path('upload-picture/', user_views.upload_profile_picture, name='upload_profile_picture'),
]



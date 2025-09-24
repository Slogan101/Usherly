from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UsherProfile, HostProfile, CustomUser



class UserRegistrationForm(UserCreationForm):
    USER_TYPES = (
        ('usher', 'Usher'),
        ('host', 'Host'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPES, widget=forms.RadioSelect)
    full_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    # organization = forms.CharField(max_length=200, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone', 'user_type', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
        user.email = self.cleaned_data['email']
        # You've chosen to make the username same as the email
        # user.username = self.cleaned_data['email'] 
        user.full_name = self.cleaned_data['full_name']
        

        if commit == True:
            user.save()

            phone = self.cleaned_data['phone']

            if user.user_type == 'usher':
                profile, _ = UsherProfile.objects.get_or_create(user=user)
                profile.phone = phone
                profile.save()
                # user.usher_profile.phone = phone
                # user.usher_profile.save()

            elif user.user_type == 'host':
                profile, _ = HostProfile.objects.get_or_create(user=user)
                profile.phone = phone
                profile.save()
                # user.host_profile.phone = phone
                # user.host_profile.save()
        #         UsherProfile.objects.create(
        #             user = user,
        #             phone = phone,
        #         )
        #     elif user.user_type == 'host':
        #         HostProfile.objects.create(
        #             user = user,
        #             phone = phone,
        #         )
        # return user
    



class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}))


class UsherUpdateForm(forms.ModelForm):
    class Meta:
        model = UsherProfile
        fields = ['age', 'height', 'phone', 'complexion', 'bio', 'profile_picture', 'photo_1', 'photo_2', 'photo_3', 'photo_4']
from django import forms
from .models import Events



class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'event_image', 'event_type', 'state', 'event_duration', 'event_description', 'pay_amount', 'event_date']
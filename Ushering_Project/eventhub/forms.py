from django import forms
from .models import Events
from django.utils import timezone



class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'event_image', 'event_type', 'state', 'event_duration', 'event_description', 'pay_amount', 'event_date', 'event_mode', 'ushers_required']

    def clean_event_date(self):
        event_date = self.cleaned_data['event_date']
        if event_date < timezone.now():
            raise forms.ValidationError("You cannot select a past date for the event.")
        return event_date
    
class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'event_image', 'event_type', 'state', 'event_duration', 'event_description', 'pay_amount', 'event_date', 'event_mode', 'ushers_required']
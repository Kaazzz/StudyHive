from django import forms
from .models import CalendarEvent
from django.core.exceptions import ValidationError

class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'description', 'start_time', 'end_time',]  # Include all fields from the model

        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            start_time = cleaned_data.get('start_time')
            end_time = cleaned_data.get('end_time')
            if start_time and end_time and start_time >= end_time:
                raise ValidationError("End time cannot be before start time.")
            return cleaned_data

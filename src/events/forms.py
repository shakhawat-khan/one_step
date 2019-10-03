from django import forms
from django.contrib.admin import widgets         
from django.contrib.auth.models import User
from .models import Event

class DateInput(forms.DateInput):
    input_type = 'date'

class EventCreateForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['title', 'about', 'area', 'eventTime', 'thumbnail']
        widgets = {'eventTime': widgets.AdminDateWidget}

from django import forms
from django.contrib.auth.models import User
from .models import Donation

class CauseDonateForm(forms.ModelForm):

    class Meta:
        model = Donation
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'donate_amount']

class CauseByBudgetForm(forms.Form):

    maxBudget = forms.IntegerField(label='Max Budget')
    minBudget = forms.IntegerField(label='Min Budget')
    class Meta:
        
        fields = ['maxBudget', 'minBudget']
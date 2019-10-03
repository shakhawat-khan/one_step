from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from .models import Post,Comment
from causes.models import Catagory


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]


 
    

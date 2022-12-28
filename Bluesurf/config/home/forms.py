from dataclasses import fields
from tkinter import Widget
from django import forms
from crispy_forms.helper import FormHelper
from django.core import validators
from django.forms import CharField, Textarea
from django.contrib.auth.models import User
from home.models import sortCategory

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'newpassword','placeholder':"Pasword"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'size': '30','placeholder':"Email"}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        help_texts = {
        'username': None
        }
        widgets = {
            'first_name':forms.TextInput(attrs={'placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'placeholder':'Last Name'}),
            'username':forms.TextInput(attrs={'placeholder':'Username'}),
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Password"}))
   


class sortForm(forms.ModelForm):
    category = forms.ModelChoiceField(label=('SORT BY:'),queryset= sortCategory.objects.all())
    class Meta():
        model = sortCategory
        fields = ("category",)
    


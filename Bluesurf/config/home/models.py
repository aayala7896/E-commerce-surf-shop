from django.db import models

# Create your models here.
from dataclasses import fields
from tkinter import Widget
from django import forms
from crispy_forms.helper import FormHelper
from django.core import validators
from django.forms import CharField, Textarea
from django.contrib.auth.models import User


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

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
   
class Product(models.Model):
    name = models.CharField(max_length=255)
    id = models.BigAutoField(primary_key=True)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=128)
    image = models.ImageField(upload_to=upload_to,blank=True,null=True)


class sortCategory(models.Model):
    category = models.CharField(max_length = 128)
    def __str__(self):
        return self.category

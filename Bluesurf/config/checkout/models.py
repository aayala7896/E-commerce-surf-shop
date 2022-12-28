from django.db import models

# Create your models here.
from dataclasses import fields
from tkinter import Widget

from crispy_forms.helper import FormHelper
from django.core import validators
from django.forms import CharField, Textarea
from django.contrib.auth.models import User
from home.models import Product
from django.core import validators
from django.utils import timezone
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    orderTotal = models.PositiveIntegerField()
    dataPurchased = models.DateTimeField(default=timezone.now)
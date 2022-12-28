import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from cart.cart import Cart
from home.models import Product
from checkout.models import Order
from home.views import cart_clear
from django.shortcuts import render, redirect
from home.models import Product,User
from requests import request
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url='/login/')
def Orders(request):
    table_data = Order.objects.filter(user=request.user)
    context = {
        "table_data": table_data,
    }

    return render(request,'checkoutpage/order.html',context)

@login_required(login_url='/login/')
def PaymentPageView(request):
    cartTotal=0
    for id,item in request.session['cart'].items():
        cartTotal = cartTotal + int(item['quantity'])*int(item['price'])
    context={
        "cartTotal":cartTotal
    }
    return render(request,'checkoutpage/payment.html', context)

@login_required(login_url='/login/')
def charge(request):
    if request.method == 'POST':
        cartTotal=0
        for id,item in request.session['cart'].items():
            cartTotal = cartTotal + int(item['quantity'])*int(item['price'])
        charge = stripe.Charge.create(
            amount=cartTotal,  # amount is in cents.
            currency='usd',
            description='Check Out',
            source=request.POST['stripeToken']
        )
        user = User.objects.get(id=request.user.id)
        Order(user=user, orderTotal=cartTotal).save()
        cart = Cart(request)
        cart.clear()
        table_data= Order.objects.filter(user=request.user).latest('id')
        context={
            "table_data":table_data
         }
      
        return render(request, 'checkoutpage/charge.html',context)




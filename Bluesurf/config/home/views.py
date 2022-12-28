from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests import request
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from home.models import Product,User,sortCategory
from home.forms import sortForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from home.forms import JoinForm,LoginForm

from home.serializers import UserSerializer,ProductSerializer
from cart.cart import Cart



#rest_framework viewsets

class ProductEntryViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
   

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
# Create your views here.


def home(request):
    table_data = Product.objects.all()

    if(sortCategory.objects.count() == 0):
        sortCategory(category="Alphabetically").save()
        sortCategory(category="Price,low to high").save()
        sortCategory(category="Price,high to low").save()
    if(request.method == "GET" and "category" in request.GET):
            cat = request.GET
            if(cat["category"] == '1'):
                table_data= Product.objects.all().order_by('name')
            elif(cat["category"] == '2'):
                table_data= Product.objects.all().order_by('price')
            elif(cat["category"] == '3'):
                table_data= Product.objects.all().order_by('-price')
  
    context={
            "table_data":table_data,
            "form":sortForm
    }
    
    return render(request,'homepage/home.html',context)

def user_join(request):
    if(request.method == "POST"):
        join_form = JoinForm(request.POST)
        if(join_form.is_valid()):
            user = join_form.save()
            user.set_password(user.password);
            user.save()
            return redirect("/")
        else:
            page_data = {"join_form":join_form}
            return render(request,'homepage/join.html',page_data)
    else:
        join_form = JoinForm()
        page_data = {"join_form":join_form}
        return render(request,'homepage/join.html',page_data)

def user_login(request):
	if(request.method == 'POST'):
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			username = login_form.cleaned_data["username"]
			password = login_form.cleaned_data["password"]
			user = authenticate(username = username,password = password)
			if user:
				if user.is_active:
					login(request,user)
					return redirect("/")
				else:
					return HttpResponse("Your account is not active.")
			else:
				print("Someone tried to login and failed.")
				print("They used username: {} and password: {}".format(username,password))
				return render(request, 'homepage/login.html', {"login_form": LoginForm})
	else:
		return render(request, 'homepage/login.html', {"login_form": LoginForm})

def user_logout(request):
	logout(request)
	return redirect("/")

def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product = product)

    return redirect("home")

@login_required(login_url='/login/')
def cart_detail(request):
    cartTotal = 0
    if not request.session.get('cart', None):
        context={
                    "cartTotal":cartTotal
        }
        return render(request,'cartpage/cart.html',context)

    else:
        for id,item in request.session['cart'].items():
            cartTotal = cartTotal + int(item['quantity'])*float(item['price'])/100
    
            context={
                    "cartTotal":cartTotal
            }
    
    return render(request,'cartpage/cart.html',context)

def item_remove(request,id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product=product)
    return redirect("cart_detail")

def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url='/login/')
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url='/login/')
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

def about_me(request):
	return render(request,'homepage/about.html')
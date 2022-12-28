"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views as home_views
from checkout import views as checkout_views
from django.urls import include,path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static



router = routers.DefaultRouter()
router.register(r'product-entries',home_views.ProductEntryViewSet)
router.register(r'users',home_views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_views.home, name="home"),
    path('cart/add/<int:id>/', home_views.cart_add, name='cart_add'),
    path('cart/item_increment/<int:id>/',home_views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',home_views.item_decrement, name='item_decrement'),
    path('cart/item_clear/<int:id>/', home_views.item_remove, name='item_remove'),
    path('cart/cart-detail/',home_views.cart_detail,name='cart_detail'),
    path('api/v1/', include(router.urls)),
    path('api-auth/v1/', include('rest_framework.urls', namespace='rest_framework')),
    path('join/',home_views.user_join),
    path('login/', home_views.user_login),
    path('logout',home_views.user_logout),
 
    path('payment/', checkout_views.PaymentPageView, name='payment'),
    path('charge/', checkout_views.charge, name='charge'),
    path('orders/', checkout_views.Orders,name= 'orders'),
    path('about/', home_views.about_me),
    

   

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

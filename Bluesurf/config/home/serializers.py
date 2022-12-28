from home.models import Product
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields =['username','email']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        user = UserSerializer
        model = Product
        fields = '__all__'
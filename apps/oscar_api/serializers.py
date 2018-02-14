from apps.catalogue.models import Product
from apps.friendship.models import FriendShip
from rest_framework import serializers
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined')

class FriendShipListSerializer(serializers.ModelSerializer):
    friend = serializers.Field(source='to_json')
    class Meta:
        model = FriendShip
        fields = ('id', 'user_self', 'user_obj', 'type', 'friend')

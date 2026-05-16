from rest_framework import serializers
from .models import Order, OrderItem,Address


# 🔹 OrderItem Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'title','image', 'price', 'qty']

class AddressMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'full_name',
            'phone',
            'address_line1',
            'city',
            'state',
            'pincode'
        ]


# 🔹 Order Serializer (with nested items)
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True,)
    address = AddressMiniSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'total', 'address','status', 'created_at', 'items']



# wishlist
from rest_framework import serializers
from .models import Wishlist

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'


from rest_framework import serializers
from .models import Address

# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         fields = '__all__'
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        extra_kwargs = {
            'full_name': {'required': False},
            'phone': {'required': False},
            'email': {'required': False},
            'address_line1': {'required': False},
            'state': {'required': False},
        }

from rest_framework import serializers
from django.contrib.auth.models import User

# 🔹 USER SERIALIZER
from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"



from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
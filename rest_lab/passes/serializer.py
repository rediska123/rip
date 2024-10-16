from rest_framework import serializers
from passes.models import *

class OrderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    m_username = serializers.CharField(source='moderator.username')
    class Meta:
        # Модель, которую мы сериализуем
        model = PassOrder
        # Поля, которые мы сериализуем
        fields = ["id", "name", "phone",  "accepted_date", "created_date",  "status", "submited_date", "username", "m_username"]


class PassSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = PassItem
        # Поля, которые мы сериализуем
        fields = ["id", "name", "description", "price", "image", "status"]


class OrderItemSerializer(serializers.ModelSerializer):
    pass_name = serializers.CharField(source='pass_item.name')
    pass_price = serializers.CharField(source='pass_item.price')
    class Meta:
        # Модель, которую мы сериализуем
        model = PassOrderItems
        # Поля, которые мы сериализуем
        fields = ["pass_name", "pass_price", "amount", "id"]
    

class OrderDetailsSerializer(serializers.ModelSerializer):
    passes = OrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username')
    class Meta:
        # Модель, которую мы сериализуем
        model = PassOrder
        # Поля, которые мы сериализуем
        fields = ["id", "name", "phone", "created_date", "submited_date", "accepted_date", "status", "passes", "username"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = AuthUser
        # Поля, которые мы сериализуем
        fields = ["username", "password", "email"]


class EditUserSerializer(serializers.ModelSerializer):
    passes = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        # Модель, которую мы сериализуем
        model = AuthUser
        # Поля, которые мы сериализуем
        fields = ["first_name", "last_name", "email", "password", "passes"]


class EditOrderSerializer(serializers.ModelSerializer):
    passes = PassSerializer(many=True, read_only=True)
    class Meta:
        # Модель, которую мы сериализуем
        model = PassOrder
        # Поля, которые мы сериализуем
        fields = ["name", "phone", "created_date", "passes"]

class EditOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = PassOrderItems
        # Поля, которые мы сериализуем
        fields = ["id", "product_id", "order", "amount"]
from rest_framework import serializers
from passes.models import *

class ClientCardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    moderator = serializers.CharField(source='moderator.username', allow_null=True)
    class Meta:
        # Модель, которую мы сериализуем
        model = PassOrder
        # Поля, которые мы сериализуем
        fields = ["id", "name", "phone",  "accepted_date", "created_date",  "status", "submited_date", "username", "moderator"]


class PassSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = PassItem
        # Поля, которые мы сериализуем
        fields = ["id", "name", "description", "price", "image", "status"]


class ClientCardPassSerializer(serializers.ModelSerializer):
    pass_name = serializers.CharField(source='pass_item.name')
    pass_price = serializers.CharField(source='pass_item.price')
    class Meta:
        # Модель, которую мы сериализуем
        model = PassOrderItems
        # Поля, которые мы сериализуем
        fields = ["pass_name", "pass_price", "amount", "id"]
    

class ClientCardDetailsSerializer(serializers.ModelSerializer):
    passes = ClientCardPassSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username')
    class Meta:
        # Модель, которую мы сериализуем
        model = PassOrder
        # Поля, которые мы сериализуем
        fields = ["id", "name", "phone", "created_date", "submited_date", "accepted_date", "status", "passes", "username"]


class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)
    class Meta:
        # Модель, которую мы сериализуем
        model = User
        # Поля, которые мы сериализуем
        fields = ["username", "password", "email", "is_staff", "is_superuser", "first_name", "last_name"]

    def create(self, validated_data):
        user = super().create(validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user


class EditUserSerializer(serializers.ModelSerializer):
    passes = ClientCardPassSerializer(many=True, read_only=True)
    class Meta:
        # Модель, которую мы сериализуем
        model = User
        # Поля, которые мы сериализуем
        fields = ["first_name", "last_name", "email", "password", "passes"]


class EditClientCardSerializer(serializers.ModelSerializer):
    passes = PassSerializer(many=True, read_only=True)
    class Meta:
        # Модель, которую мы сериализуем
        model = PassOrder
        # Поля, которые мы сериализуем
        fields = ["name", "phone", "created_date", "passes"]

class EditClientCardPassSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = PassOrderItems
        # Поля, которые мы сериализуем
        fields = ["id", "product_id", "order", "amount"]
from product.models import Product
from .models import AllShop, Savdo, Klient, CommentaryStatus, TashkilotYaratish
from rest_framework import serializers
from django.contrib.auth import get_user_model


class KlientSerialzier(serializers.ModelSerializer):
    client_user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Klient
        fields = [
            "id",
            "mobile",
            "client_user",
            "clientStatusupdate",
            "clientFoizstatus",
        ]

    def get_client_user(self, obj):
        return {
            "id": obj.client_user.id,
            "phone": obj.client_user.phone,
            "first_name": obj.client_user.first_name,
            "last_name": obj.client_user.last_name,
        }


class AllShopSerializers(serializers.ModelSerializer):
    userId = serializers.SerializerMethodField(read_only=True)
    nastroyka = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AllShop
        fields = "__all__"

    def get_userId(self, obj):
        return {
            "id": obj.userId.id,
            "phone": obj.userId.phone,
            "password": obj.userId.shop_password,
        }
    def get_nastroyka(self, obj):
        if obj.nastroyka is not None:
            return {
                "skidka": obj.nastroyka.skidka
            }
        else:
            return {
                "skidka": None
            }



class DokonCreateSerializer(serializers.Serializer):
    foydalanuvchi_ism = serializers.CharField(max_length=200)
    phone = serializers.CharField(
        max_length=12,
        min_length=12,
    )
    password = serializers.CharField(max_length=100)
    shop_password = serializers.CharField(max_length=200)
    foydalanuvchi_familya = serializers.CharField(max_length=200)
    shop_status = serializers.BooleanField(default=False)
    vendor = serializers.BooleanField(default=False)
    shop_name = serializers.CharField(max_length=200)
    vendor = serializers.BooleanField(default=False)
    sklad = serializers.BooleanField(default=False)

    def validate_phone(self, value):
        from re import match

        if not match("^998\d{2}\s*?\d{3}\s*?\d{4}$", value):
            raise serializers.ValidationError("Invalid phone number.")

        return value


class DokonLoginSerialzier(serializers.Serializer):
    phone = serializers.CharField(
        max_length=12,
        min_length=12,
    )
    password = serializers.CharField(max_length=100)
    shop_passwords = serializers.CharField(max_length=50, required=False)

    def validate_phone(self, value):
        from re import match

        if not match("^998\d{2}\s*?\d{3}\s*?\d{4}$", value):
            raise serializers.ValidationError("Invalid phone number.")

        return value


class CLientFilterPhoneSerialzier(serializers.Serializer):

    phone = serializers.CharField(
        max_length=12,
        min_length=12,
    )

    def validate_phone(self, value):
        from re import match

        if not match("^998\d{2}\s*?\d{3}\s*?\d{4}$", value):
            raise serializers.ValidationError("Invalid phone number.")

        return value


class TashkilotSerializers(serializers.ModelSerializer):
    class Meta:
        model = TashkilotYaratish
        fields = "__all__"


class CheckProductPUTSerialzier(serializers.Serializer):
    status = serializers.BooleanField(default=False)
    tekshiruvId = serializers.IntegerField()
    products = serializers.JSONField(required=False)


class ProductCheckSerialzier(serializers.Serializer):
    id = serializers.IntegerField()
    present_count = serializers.IntegerField(required=False)
    present_serena = serializers.ListField(required=False)

class ALlShopProductserializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","product_name", "serenaTrue_countFalse", "dokon_tavarlar"]
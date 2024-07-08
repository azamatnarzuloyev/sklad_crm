from os import access
from django.contrib.auth import get_user_model
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from .models import Address , GouseUser , User


class GostSerialzier(serializers.ModelSerializer):
    class Meta:
        model = GouseUser
        fields = "__all__"

class DeviseSerialzier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "divase"]


class DokonAuthenticationSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=12,
        min_length=12,
    )
    # password =  serializers.CharField(max_length=100)
    shop_password = serializers.CharField(max_length=200)

    def validate_phone(self, value):
        from re import match

        if not match("^998\d{2}\s*?\d{3}\s*?\d{4}$", value):
            raise serializers.ValidationError("Invalid phone number.")

        return value
    
class DokonSuperAuthenticationSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=12,
        min_length=12,
    )
    # password =  serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=200)

    def validate_phone(self, value):
        from re import match

        if not match("^998\d{2}\s*?\d{3}\s*?\d{4}$", value):
            raise serializers.ValidationError("Invalid phone number.")

        return value




class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id", "phone",
            # "first_name", "last_name",
            # "author",
        ]


class UserDetailUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = [
            "password",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    phone = serializers.ReadOnlyField()
    
    class Meta:
        model = get_user_model()
        fields = [
            "id", "phone",
            "first_name", "last_name",
            "two_step_password", "vendor_user",
        ]


class AuthenticationSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=12,
        min_length=12,
    )

    def validate_phone(self, value):
        from re import match

        if not match("^998\d{2}\s*?\d{3}\s*?\d{4}$", value):
            raise serializers.ValidationError("Invalid phone number.")

        return value
    

class MobileAuthenticationSerializers(serializers.Serializer):
    phone = serializers.CharField(
        max_length=12,
        min_length=12,
    )
    shop_password = serializers.CharField(max_length=100)

    def validate_phone(self, value):
        from re import match

        if not match("^998\d{2}\s*?\d{3}\s*?\d{4}$", value):
            raise serializers.ValidationError("Invalid phone number.")

        return value


class OtpSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=6,
        min_length=6,
    )
    two_step_passwords = serializers.CharField(max_length=40, required=False, default=None)
    
    def validate_code(self, value):
        try:
            int(value)
        except ValueError as _:
            raise serializers.ValidationError("Invalid Code.")

        return value


class CreateTwoStepPasswordSerializer(serializers.Serializer):
    """
        Base serializer two-step-password.
    """
    new_password = serializers.CharField(
        max_length=20,
    )

    confirm_new_password = serializers.CharField(
        max_length=20,
    )

    def validate(self, data):
        password = data.get('new_password')
        confirm_password = data.get('confirm_new_password')

        if password != confirm_password:
            raise serializers.ValidationError(
                {"Error": "Your passwords didn't match."}
            )

        return data


class ChangeTwoStepPasswordSerializer(CreateTwoStepPasswordSerializer):
    old_password = serializers.CharField(
        max_length=20,
    )



class AddressSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user']
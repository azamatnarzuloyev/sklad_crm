from magazin.models import AllShop, Savdo , DaySellerShop ,Klient
from product.models import Product 
from rest_framework import serializers
from datetime import date
from django.utils import timezone
from .models import TechnicalStaff , InstallationService
from django.core.files.base import ContentFile


class SavdoUpdateSerialziers(serializers.Serializer):
    id = serializers.UUIDField()
    summaUpdate = serializers.DictField()
    vazvrat = serializers.DictField()
    TavarUpdate = serializers.DictField()
    notification = serializers.DictField()
    tashkilot_update = serializers.DictField()

class ClientAuthenticationSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=12,
        min_length=12,
    )
    def validate_phone(self, value):
        from re import match

        if not match("^998\d{2}\s*?\d{3}\s*?\d{4}$", value):
            raise serializers.ValidationError("Invalid phone number.")

        return value



class ClientSerializers(serializers.ModelSerializer):
    client_user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Klient
        fields = ["id", "mobile", "clientStatusupdate", "clientFoizstatus", "status_client", "client_user",  'savdo_sum', 'hamyon_client_data', 'qarzdorlik_fn',]

    def get_client_user(self, obj):
        if obj.client_user is not None:
            return {
                
                "user_id": obj.client_user.id,
                "first_name": obj.client_user.first_name,
                "last_name": obj.client_user.last_name
            }
        return None


#------------- savdo get serailizers -----------------------------


class DaySellerShopSerialziers(serializers.ModelSerializer):
    class Meta:
        model = DaySellerShop
        fields = "__all__"


class DaySellerShopSerialziersMobile(serializers.ModelSerializer):
    # products = serializers.ReadOnlyField(required=False, default=None)
    # getClient= serializers.SerializerMethodField(read_only=True)
    client_uuid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DaySellerShop
        fields = "__all__"
   
    def get_client_uuid(self, obj):
        if obj.client_uuid is not None:
            return {
                "id": obj.client_uuid.id,
                "name": obj.client_uuid.client_user.first_name,
                "last_name": obj.client_uuid.client_user.last_name
            }
      




class SavdoSerializer(serializers.ModelSerializer):
    createdateseller = DaySellerShopSerialziers(read_only=True, many=True)
    class Meta:
        model  = Savdo
        fields = "__all__"


# -----------savdo post serializers -----------------------------------



class OtpSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=6,
        min_length=6,
    )

    def validate_code(self, value):
        try:
            int(value)
        except ValueError as _:
            raise serializers.ValidationError("Invalid Code.")

        return value




class DeyShopSellerSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    sum_paid = serializers.FloatField(default=0)
    savdo_yopish = serializers.BooleanField(default=False)
    cashback_sum = serializers.FloatField(default=0)
    qarzdorlik_summa = serializers.FloatField(default=0)
    toliqQarzga = serializers.BooleanField(default=False)
    sellerclose_date = serializers.DateTimeField(default=timezone.now())
    skidka_price = serializers.FloatField(default=0)
    product_arr = serializers.JSONField(required=False, default=None)
    
    def validate(self, data):
        id =  data.get('id')
        if DaySellerShop.objects.filter(id=id).exists:
            return data
        else:
            return serializers.ValidationError("errors id not fount")
    





class DeleteSavdoSerializer(serializers.Serializer):
    allProductDelete = serializers.BooleanField(default=False)
    deleteSavdo_data = serializers.DateField(default=date.today())
    daySavdo_id  = serializers.UUIDField()
    product_ids = serializers.JSONField(required=False, default={})
    



class UserDataUpdateSerialzier(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    cashback_kard = serializers.IntegerField()
    random_status = serializers.BooleanField(default=False)
    phone = serializers.CharField( max_length=12,
        min_length=12,)
    # depozit_card = serializers.IntegerField(required=False, default=None)
    def validate_phone(self, value):
        from re import match

        if not match("^998\d{2}\s*?\d{3}\s*?\d{4}$", value):
            raise serializers.ValidationError("Invalid phone number.")

        return value
    




class CashbackUpdateSerialalizer(serializers.Serializer):
    client_id = serializers.IntegerField()
    day_savdoId = serializers.UUIDField()
    depozit_sum = serializers.FloatField( required=False,default=None)




class TechnicalStafSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalStaff
        fields = "__all__"


class InstallationServiceSerialzier(serializers.ModelSerializer):
    class Meta:
        model = InstallationService
        fields = "__all__"


class CashbackUserDataUpdateSerialzier(serializers.Serializer):
    firt_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    cashback_kard = serializers.IntegerField()
    random_status = serializers.BooleanField(default=False)


  



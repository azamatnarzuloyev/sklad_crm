from puttyMagazin.models import  DokonPutty, TavarPutty
from rest_framework import serializers
from magazin.models import AllShop


class ListSerialzier(serializers.ListField):
    id = serializers.IntegerField()
    product_count = serializers.IntegerField()
    product_serena = serializers.ListField()
    product_price = serializers.FloatField()
    material_nomer = serializers.IntegerField()

            
class PostPuttyProductSerializer(serializers.ModelSerializer):
    shop_id = serializers.UUIDField()

    class Meta:
        model = TavarPutty
        fields = "__all__"




class GetTavarPuttySerialzier(serializers.ModelSerializer):
    class Meta:
        model = TavarPutty
        fields = "__all__"





class VendorProductSerializer(serializers.Serializer):
    putty_id = serializers.UUIDField()

    putty_status = serializers.BooleanField(default=False)

    # def validate(self, data):

    #     putty_id = data.get('putty_id')

    #     putty = TavarPutty.objects.filter(putty_status=False, id=putty_id).exists()

    #     if putty:
    #         return data
    #     else:
    #         raise serializers.ValidationError({
    #             "putty_id or shop_id": "errors" 
    #         })


class PuttyDeleteSerializer(serializers.Serializer):
    putty_id = serializers.UUIDField()
    
    def validate(self, data):
        putty_id = data.get('putty_id')
        print(TavarPutty.objects.filter(putty_status=False, id=putty_id).exists())
        if TavarPutty.objects.filter(putty_status=False, id=putty_id).exists():
            return data
        else:
            raise serializers.ValidationError(
               {  "errors": "putty is not delete"}
            )
 

    
class GetPuttySerialzier(serializers.Serializer):
    shop_id = serializers.UUIDField(default=None)
    putty_status = serializers.BooleanField(default=False)
    send_maagzinId = serializers.UUIDField(default=None) 
    sendMagazinIdToken = serializers.BooleanField(default=False)   

      
class GetTestPuttySerialzier(serializers.Serializer):
    shop_id = serializers.UUIDField(required=False)
    putty_status = serializers.BooleanField(default=False)
    send_maagzinId = serializers.UUIDField(required=False) 
    sendMagazinIdToken = serializers.BooleanField(default=False)   

class VendorTavarlar(serializers.ModelSerializer):
    class Meta:
        model = DokonPutty
        fields = "__all__"
        






    















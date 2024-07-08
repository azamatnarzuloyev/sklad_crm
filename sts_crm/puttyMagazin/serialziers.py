from rest_framework import serializers
from .models import  TavarPutty, DokonPutty , ZakasProduct
from datetime import date, datetime

class ProductPuttyVerifySerialzier(serializers.Serializer):
    id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=200,)
    date_today = serializers.DateField(default=date.today)

    


    
    def validate(self, data):
        product_counts = data.get('product_count')
        serena = data.get('serena')
        if product_counts and serena:
            raise serializers.ValidationError( { "data": None,"errors": True, "message": "serena bilan product count birga bo'lolmaydi"})
        return data
      


       





class PuttyQabulSerailizers(serializers.Serializer):
    id  = serializers.CharField(max_length=200)
    putty_status = serializers.BooleanField(default=False)
    update_date = serializers.DateTimeField(default=datetime.now)


class DokonPuttySerailziers(serializers.ModelSerializer):
    class Meta:
        model = DokonPutty
        fields = "__all__"



class ZakasProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = ZakasProduct
        fields ="__all__"


class ProductZakasSerializers(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    product_count = serializers.IntegerField()
    status = serializers.BooleanField(default=False)
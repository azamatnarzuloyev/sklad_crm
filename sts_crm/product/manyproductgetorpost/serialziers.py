from rest_framework import serializers


class ManyProductSerialzier(serializers.Serializer):
    """ many data product update serialziers """
    many_data = serializers.BooleanField(default=False)
    list_data = serializers.ListField()



class ProductPutSerialzier(serializers.Serializer):
    """ Product update serializers """
    id = serializers.IntegerField()
    serenaTrue_countFalse = serializers.BooleanField(default=None)
    product_serena = serializers.ListField(default=None)
    product_count = serializers.IntegerField(default=None)




class ProductPostSerialzier(serializers.Serializer):
    """ Product post serializers """
    serenaTrue_countFalse = serializers.BooleanField()
    # product_serena = serializers.ListField(required=False)
    # product_count = serializers.IntegerField(required=False)
    product_name = serializers.CharField()


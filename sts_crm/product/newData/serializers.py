from rest_framework import serializers
from product.models import Product
from magazin.models import AllShop



class AllShopSerialziers(serializers.ModelSerializer):
    class Meta:
        model = AllShop
        fields = "__all__"

class ProductsSerialziersJson(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

 

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self,obj, *args, **kwargs):
        self.obj = obj
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class ProductsShopSerialziersJson(serializers.ModelSerializer):
    # dokon = serializers.SerializerMethodField()
    # get_dokonlar = serializers.SerializerMetaclass()
    class Meta:
        model = Product
        fields = ['id', "price",  "material_nomer", "serenaTrue_countFalse", "tavar_ckidka", "site_sts", "site_rts", "discount_price", "product_picture", "product_name", "dokon_tavarlar",]

    # def get_dokon(self, obj):
    
    #     product_count  = Product.objects.count()
    #     shop  = AllShop.objects.all()
     
    #     return product_count

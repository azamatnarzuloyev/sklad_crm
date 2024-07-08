from rest_framework import serializers
from .models import Product, ProductNewsImport, TavarTekshiruv
from datetime import date


# -------------------------------------------------------


class ProductShopserializer(serializers.ModelSerializer):
    """do'kon ichidagi tavarlarni ko'rish uchun tavar madellari"""

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "material_nomer",
            "serenaTrue_countFalse",
            "price",
            "discount_price",
            "tavar_ckidka",
        ]


# ----------------------------------------------------------------------


class StringListField(serializers.ListField):
    """bitta tavarnidagi serena qo'shish uchun api"""

    serena = serializers.IntegerField(allow_null=True)


class PhotoSerializer(serializers.Serializer):
    product_picture = serializers.ImageField()


class ProductSerializer(serializers.ModelSerializer):
    """product yangilash va bitta  tavar uchun api"""

    # productShop = ProductDetailShopSerializers(many=True, read_only=True)
    product_serena = StringListField(read_only=True)
    product_count = serializers.IntegerField(read_only=True)
    shop_id = serializers.CharField(max_length=300, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


# -------------------------------------------------------------------------------


class ProductDetailSerializer(serializers.ModelSerializer):
    """! productni ko'rish"""

    product_serena = StringListField(read_only=True)
    product_count = serializers.IntegerField(read_only=True)
    shop_id = serializers.CharField(max_length=300, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


# ------------------------------------------------------------------


class ShopStringserializers(serializers.ListField):
    """barcha tavarlarni qo'shish uchun madel"""

    product_serena = StringListField(read_only=True)
    shop_id = serializers.CharField(max_length=300, read_only=True)
    product_count = serializers.IntegerField(read_only=True)


class ProductPostSerializer(serializers.ModelSerializer):
    """Barcha tavarlarni yaratish"""

    shop_serena = ShopStringserializers(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


# -----------------------------------------------------------------------


class DokonProductSerializers(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "product_name", "material_nomer"]


class ProductjsonFiledSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "articul",
            "dokon_tavarlar",
            "site_sts",
            "site_rts",
            "price",
            "discount_price",
        ]


class NewImportProductSerialzier(serializers.ModelSerializer):
    class Meta:
        model = ProductNewsImport
        fields = [
            "import_id",
            "commentary",
            "create_at",
            "datetime_create",
            "createStatus_number",
            "products",
            "close_data",
            "shop_id",
            "file_url",
        ]


class TavarTekshiruvSerialzier(serializers.ModelSerializer):
    class Meta:
        model = TavarTekshiruv
        fields = "__all__"

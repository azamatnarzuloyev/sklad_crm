from rest_framework import serializers
from .models import SuperCategory , MainCategory , SubCategory






class SuperCategorySerialzier(serializers.ModelSerializer):
    class Meta:
        model = SuperCategory
        fields = [ "id", "super_name", "slug", "meta_name", "meta_content", "sts_site", "rts_site"]





class MainCategorySerialzeir(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = ["id","main_name", "slug", "main_meta", "main_content", "sts_site", "rts_site", "superCategory"]




class SubCategorySeriazler(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id" , "sub_name", "mainCategory", "sub_image", "slug"]
    
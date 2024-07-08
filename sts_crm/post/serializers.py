from rest_framework import serializers
from .models import Istoriya



class IstoriyaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Istoriya
        fields = "__all__"
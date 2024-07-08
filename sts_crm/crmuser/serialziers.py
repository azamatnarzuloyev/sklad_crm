from rest_framework import serializers
from .models import CrmUserModels , KunYopish , XabarlarHujjatlar

class SRmUserModelsSerialzier(serializers.ModelSerializer):
    class Meta:
        model = CrmUserModels
        fields= "__all__"



from rest_framework import serializers
from .models import Hamyon, Kard , DepozitCarddata


class DepozitSerialzier(serializers.ModelSerializer):
    class Meta:
        model = DepozitCarddata
        fields = "__all__"

class KartSerializer(serializers.ModelSerializer):
    kard_cod = serializers.ReadOnlyField()
    class Meta:
        model = Kard
        fields = ('id', 'kard_cod','activae_kard','karta_sum', 'karta_sum', 'karta_random', 'kardSumma_arxiv')


class PostSerializer(serializers.ModelSerializer):
    kard = KartSerializer(many=True, read_only=True)
    depozitcardId = DepozitSerialzier(read_only=True)
    class Meta:
        model = Hamyon
        fields = ('id',  'activete', 'kard', 'money', 'karta_date', 'depozitcardId')



class UpdatehamyonSerialzier(serializers.Serializer):

    depozit_id = serializers.IntegerField(required=False, default=None)

    kard_id = serializers.UUIDField(required=False, default=None)

    hamyon_id = serializers.IntegerField()

    summa = serializers.FloatField(required=False, default=None)

    depozit_sum = serializers.FloatField(required=False, default=None)

    def validate(self, data):
        id =  data.get('hamyon_id')
        if Hamyon.objects.filter(id=id).exists():
            return data
        else:
            return serializers.ValidationError("errors id not fount")
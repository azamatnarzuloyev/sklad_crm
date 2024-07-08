from rest_framework.views import APIView
from rest_framework import status
from magazin.models import AllShop, DaySellerShop, Savdo 
from drf_spectacular.utils import extend_schema

from savdo.serializers import SavdoUpdateSerialziers
from rest_framework.response import Response


{
    "id": "",
    "summaUpdate":{
        "qarzdorlikUchunTolov": "",
        "depozit_summa": ""
        },
    "vazvrat": {},
    "TavarUpdate":{},
    "notification":{},
    "tashkilot_update":{},
}


class SavdoUpdateViews(APIView):
    @extend_schema(
            request=None,
            responses=None
    )
    def put(self, request, format=None):
       serialzier = SavdoUpdateSerialziers(data=request.data)
       if serialzier.is_valid():
           return Response({"data":"success"})
       return Response(serialzier.errors)
        
                







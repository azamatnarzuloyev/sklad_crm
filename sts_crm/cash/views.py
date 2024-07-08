from rest_framework.response import Response
from .models import Hamyon, Kard
from .serializers import KartSerializer, PostSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework import status  , permissions
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as fil
from rest_framework import generics, filters

from magazin.models import DaySellerShop, Klient
from savdo.serializers import DaySellerShopSerialziers
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect , csrf_exempt
from rest_framework.request import Request
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def request_dataset(request:Request):
    if request.method =='POST':
        data = request.data.get("data")
        return Response(
            {"data": "post request",
             "request": data,
             }
        )
    if request.method =='GET':
        return Response({
            "data" :"get request",
            "kamera": "kamera"
        })


class ProductFilter(fil.FilterSet):

    class Meta:
        model = Hamyon
        fields = ["id",'activete']


class HamyonListViews(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Hamyon.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["code"]
    lookup_field = "id"
 
    filter_backends = (fil.DjangoFilterBackend,)
    filterset_class = ProductFilter
   
    def get(self, request, *args, **kwargs):
        self.serializer_class = PostSerializer
        return super().get(request, *args, **kwargs)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mobile_savdolar(request):
    if request.method =='GET':
        user = request.user
        try:
            client_data = Klient.objects.get(client_user__id=user.id)
            day_savdo = DaySellerShop.objects.filter(client_uuid__id=client_data.id)
            serialzier =DaySellerShopSerialziers(day_savdo, many=True)
            return Response(serialzier.data)
        except Exception as e:
            return Response({
                "errors": f"{e}"
            })

    

@api_view(['GET'])
def site_savdo_get(request , phone):
    if request.method =='GET':
        client_data = Klient.objects.get(client_user__phone=phone)
        day_savdo = DaySellerShop.objects.filter(client_uuid__id=client_data.id)
        serialzier =DaySellerShopSerialziers(day_savdo, many=True)
        return Response(serialzier.data)






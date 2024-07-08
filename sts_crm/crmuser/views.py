from django.shortcuts import render
from rest_framework.generics import ListAPIView

from account.models import User
from .models import  CrmUserModels , GoustUsers
from .serialziers import SRmUserModelsSerialzier
from rest_framework.decorators import api_view
from magazin.models import AllShop
from magazin.serializers import AllShopSerializers
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class SrmUserModelViews(ListAPIView):
    queryset = CrmUserModels.objects.all()
    serializer_class = SRmUserModelsSerialzier


@api_view(['GET'])
def goust_userFuntion(request):
    if request.method =='GET':
        token = request.GET.get('token')
        goustBool:bool = GoustUsers.objects.filter(token=token).values('token').exists()
        if goustBool:
            goust = GoustUsers.objects.get(token=token)
            if goust.userId is not None and not(goust.online):
                # shop = AllShop.objects.get(userId__id=goust.userId)
                # shop_ser = AllShopSerializers(shop , many=False)
                users = User.objects.get(id=goust.userId)
                refresh = RefreshToken.for_user(users)
                goust.online = True
                goust.save()
                return JsonResponse({
                    "data": {
                        "access": str(refresh.access_token),
                    },
                    "status": True,
                    "errors": False,
                    "message":"",
                }, safe=False)
            if goust.userId is None:
                return JsonResponse({
                    "data": None,
                    "errors": False,
                    "status": False,
                    "message":"user not fount",
                }, safe=False)
        elif not(goustBool):
            gousts = GoustUsers()
            gousts.token = token
            gousts.save()
            return JsonResponse({
                    "data": None,
                    "errors": False,
                    "status": False,
                    "message":"user not fount",
                }, safe=False)
        else:
            return JsonResponse({
                    "data": None,
                    "errors": True,
                    "status": False,
                    "message":"token not fount",
                }, safe=False)




@api_view(['POST'])
def goust_PostFuntion(request):
    if request.method =='POST':
        user = request.user 
        token = str(request.data['token'])
        goust = GoustUsers.objects.get(token=token)
        if goust.userId is  None:
            goust.userId = int(user.id) 
            goust.save()
            return JsonResponse({
                "data": "seccess",
                "errors": False,
                "message": ""
            }, safe=False)
        return JsonResponse({
            "data": None,
            "errors": True,
            "message": ""
        })





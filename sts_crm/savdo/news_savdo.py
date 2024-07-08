from account.send_otp import  send_otp_dokon
from magazin.models import AllShop, Savdo, DaySellerShop, CommentaryStatus, Klient
from rest_framework.response import Response
from rest_framework.decorators import  api_view , permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from permission.permissions import DokonUserAuthentication
from .serializers import CashbackUserDataUpdateSerialzier, ClientAuthenticationSerializer, DaySellerShopSerialziers, ClientSerializers, SavdoSerializer, DeyShopSellerSerializer, UserDataUpdateSerialzier
from django.contrib.auth import get_user_model
from account.models import User
from rest_framework.decorators import APIView
from datetime import date
from django.utils.timezone import datetime
from product.models import Product
from cash.models import Hamyon, Kard , DepozitCarddata
from cash.serializers import PostSerializer
from drf_spectacular.utils import extend_schema
from secrets import choice as secret_choice
from string import digits
from rest_framework.permissions import IsAuthenticated 
from rest_framework.request import Request
from django.http import JsonResponse


import json

def otp_generators(size: int = 12, char: str = digits) -> str:
    return "".join(secret_choice(char) for _ in range(size))



def _errors_response(status_code, message, detail):
    data = {     
                "data": None,
                "errors": "true",
                "status": 200,
                "status_code": status_code,
                "message": message,
                "detail": detail,
                "token": "",
            },
    return JsonResponse(data, status=status_code , safe=False)



def _sesscess_respose(status_code , data, register):
    if register is not None:

        res = {
            "register": register,
            "data": data,
            "errors": "false",
            "status": 200,
            "status_code": status_code,
            "message": "",
            "detail": "",
            "token": "",
        } 
    else:
        res = {
            "data": data,
            "errors": "false",
            "status": 200,
            "status_code": status_code,
            "message": "",
            "detail": "",
            "token": "",
        } 

    return JsonResponse(res, status=status_code , safe=False)


def _test_user_phone(phone):
    """ mijozni ro'yhatdan o'tgan bo'lsa malumotlarini qaytarish"""
    client:bool = Klient.objects.filter(mobile=phone).values('mobile').exists()
    if client:
        client_data = Klient.objects.get(mobile=phone)
        serializer = ClientSerializers(client_data)
        return _sesscess_respose(status_code=200, data=serializer.data , register=False)
    else:
        return _errors_response(status_code=404 , message="mijoz malumotlarni yangilanmagan" , detail="mijoz malumotlarni update qilish kerak")
    



@api_view(['GET', 'POST'])
def client_get_or_create(request:Request):
    
    if request.method =='GET':
       
        phone = request.GET.get('phone')
        data = Klient.objects.all()
        if phone is not None:
            data = Klient.objects.filter(mobile=phone)
        serializer = ClientSerializers(data , many=True)
        
        return Response(serializer.data)
    
    if request.method =='POST':

        """ client yaratish yoki bor clientni malumotlarni qaytarish"""
        if request.data.get('phone') is None:
            return _errors_response(status_code=400, message="phone is required", detail="telefon raqam yuborish kerak")
        client_serializer =  ClientAuthenticationSerializer(data=request.data)
        if client_serializer.is_valid():
            phone = client_serializer.data.get('phone')
            user_exists:bool = get_user_model().objects.filter(phone=phone).values('phone').exists()
            if user_exists:
                return _test_user_phone(phone=phone)
            return send_otp_dokon(
                request,
                phone=phone,
            )

        return _errors_response(status_code=400, message=client_serializer.error_messages, detail=client_serializer.errors)
    

    {"first_name": "", "last_name":"", "cashback_kard":"","random_status":"", "phone":"", }
@api_view(['PUT'])
def client_data_updated_funtion(request:Request):
    if request.method =="PUT":
        """ mijozlarni ro'yhatdan o'tgandan keyin carta depozit kartasini ism familyasi kiritish uchun """
        user = request.user
        if user =='AnonymousUser':
            return _errors_response(status_code=401 , message={"token error": "user not fount"}, detail="dokon userni jo'natish kerak")
        serialzier = UserDataUpdateSerialzier(data=request.data)
        if serialzier.is_valid():
            first_name = serialzier.data.get('first_name')
            last_name = serialzier.data.get('last_name')
            cashback_kard = serialzier.data.get('cashback_kard')
            random_status = serialzier.data.get('random_status')
            phone = serialzier.data.get('phone')
            UserData = User.objects.get(phone=phone)
            UserData.last_name = last_name
            UserData.first_name = first_name
            UserData.save()
            user_hamyon:bool = Hamyon.objects.filter(id=phone).exists()
            if user_hamyon:
                hamyon = Hamyon.objects.get(id=phone)
            else:
                return _errors_response(status_code=404 , message="phone number not fount" , detail="telefon nomer xato ")
        
            if not(hamyon.activete):
                kart = Kard.objects.create(
                    kard_cod = cashback_kard,
                    karta_random = random_status,
                    activae_kard = True
                )
                kart.save()
                if hamyon.depozitcardId is  None:
                    cod = otp_generators()
                    depozit = DepozitCarddata.objects.create(
                        depozit_kard = cod,
                        depozit_random = True
                    )
                    depozit.save()
                    hamyon.depozitcardId = depozit
                
                hamyon.activete = True    
                hamyon.kard.add(kart)
                hamyon.save()
            client = Klient.objects.get(mobile=phone)
            dokon_user:bool = AllShop.objects.filter(userId__id=user.id).filter(dokon_client__id=client.pk).exists()
            if not(dokon_user):
                shops = AllShop.objects.get(userId__id=user.id).dokon_client.add(client)
                shops.save()
            hamyon_seralizer = PostSerializer(hamyon)
            client_serialzier = ClientSerializers(client)
            data = {
                "hamyon": hamyon_seralizer.data,
                "client_data": client_serialzier.data
            }
            return _sesscess_respose(status_code=202, data=data, register=None)
        return _errors_response(status_code=400, message=serialzier.error_messages , detail=serialzier.errors)


def _cashback_verify(phone , daySavdo_nomer):
    hamyon = Hamyon.objects.get(id=phone) 
    for i in hamyon.kard.all():
            if i.activae_kard and i.kardSumma_arxiv is not None:
                for j in i.kardSumma_arxiv:
                    if int(j["savdo_nomer"]) == daySavdo_nomer:
                        return j
    return None

def _hamyon_verify(phone , daySavdo_nomer):
    hamyon = Hamyon.objects.get(id=phone).depozitcardId
    
    if hamyon.activate_depozit and hamyon.depozit_arxiv is not None:
        for j in hamyon.depozit_arxiv:
            if int(j["savdo_nomer"]) == daySavdo_nomer:
                return j
    return None
    
    


api_view(['POST'])
def client_cashback_or_hamyon(request):
    if request.method =='POST':
        """
        body:   phone ,cashback_bool, hamyon_bool, daySavdo_nomer
        """
        phone = request.data.get('phone')
        cashback_bool = request.data.get('cashback_bool')
        hamyon_bool=  request.data.get('hamyon_bool')
        daySavdo_nomer = request.data.get('daySavdo_nomer')
        if cashback_bool and hamyon_bool:
            cash = _cashback_verify(phone=phone , daySavdo_nomer=daySavdo_nomer)
            hamyon = _cashback_verify(phone=phone , daySavdo_nomer=daySavdo_nomer)
            return Response({"data":{"cash":cash, "hamyon":hamyon}, "errors":True, "message": ""})
        if cashback_bool:
            cash = _cashback_verify(phone=phone , daySavdo_nomer=daySavdo_nomer)
            if cash is not None:
                return JsonResponse({"data": {"cash":cash, "hamyon":None}, "errors": False, "message": ""}, safe=False)
        if hamyon_bool:
            hamyon = _cashback_verify(phone=phone , daySavdo_nomer=daySavdo_nomer)
            if hamyon is not None:
                return JsonResponse({"data": {"cash":None, "hamyon":hamyon}, "errors": False, "message": ""}, safe=False)
        return JsonResponse({"data": None, "errors": True, "message": "data not fount"})






            
        

        
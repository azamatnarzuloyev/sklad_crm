from account.send_otp import  send_otp_dokon
from magazin.models import AllShop, Klient
from rest_framework.response import Response
from rest_framework.decorators import  api_view , permission_classes
from rest_framework import status
from permission.permissions import DokonUserAuthentication
from .serializers import CashbackUserDataUpdateSerialzier, ClientAuthenticationSerializer, ClientSerializers, UserDataUpdateSerialzier
from django.contrib.auth import get_user_model
from account.models import User
from cash.models import Hamyon, Kard , DepozitCarddata
from cash.serializers import PostSerializer
from drf_spectacular.utils import extend_schema
from secrets import choice as secret_choice
from string import digits
from rest_framework.permissions import IsAuthenticated

def otp_generators(size: int = 12, char: str = digits) -> str:
    return "".join(secret_choice(char) for _ in range(size))


def _user_test_views(request, phone):
    user= request.user
    user_exists =  User.objects.get(phone=phone)
    klient = Klient()
    klient.client_name = user_exists.first_name
    klient.mobile = user_exists.phone
    klient.save()
    client_get = Klient.objects.get(mobile=phone)
    shop_add = AllShop.objects.get(userId__id=user.id)
    shop_add.dokon_client.add(client_get)
    shop_add.save()

    hamyon = Hamyon.objects.get(id=phone)
    serializer_hamyon = PostSerializer(hamyon)
    serializer = ClientSerializers(client_get)
    data = {
        "dokon_client": True,
        "hamyon": serializer_hamyon.data,
        "mijoz_data": serializer.data,
    }
    return Response(data)

    

@extend_schema(
        request=ClientSerializers,
        responses= {
            200: ClientSerializers,
            201: ClientAuthenticationSerializer
        }
)
@api_view(['POST', 'GET'])
def client_create(request):
    if request.method =='GET':
        client = Klient.objects.all()
        serializer = ClientSerializers(client , many=True)
        return Response(serializer.data)
    """ client get or create funtion"""
    if request.method =="POST":
        data = request.data 
        user_id = request.user
        if str(user_id)=='AnonymousUser':
            return Response({
                "User token": "not valid"
            })
        serializer = ClientAuthenticationSerializer(data=data)
        if serializer.is_valid():
            phone = serializer.data.get('phone')
            dokon_userr: bool = AllShop.objects.filter(userId__phone=phone).exists()
            if dokon_userr:
                return Response({
                    "dokon foydalanuvchisi": "bu client bo'la olmaydi "
                })
 
            user_is_exists: bool = get_user_model().objects.filter(phone=phone).values("phone").exists()
            if not user_is_exists:
                return send_otp_dokon(
                request,
                phone=phone,
                )
            client: bool= Klient.objects.filter(mobile=phone).values('mobile').exists()
            if client:
                client_get = Klient.objects.get(mobile=phone)
                datashop = AllShop.objects.filter(userId__id=user_id.id, dokon_client__id= client_get.id).exists()
                if datashop:
                        hamyon = Hamyon.objects.get(id=phone)
                        serializer_hamyon = PostSerializer(hamyon)
                        serializer = ClientSerializers(client_get)
                        data = {
                            "dokon_client": True,
                            "hamyon": serializer_hamyon.data,
                            "mijoz_data": serializer.data,
                        }
                        return Response(data)
                        
                client_get = Klient.objects.get(mobile=phone)
                shop_add = AllShop.objects.get(userId__id=user_id.id)
                shop_add.dokon_client.add(client_get)
                shop_add.save()
                dokon_names = AllShop.objects.filter(dokon_client__id= client_get.id).first()
                hamyon = Hamyon.objects.get(id=phone)
                serializer_hamyon = PostSerializer(hamyon)
                serializer = ClientSerializers(client_get)
                data_Set = {
                    "dokon_client": False,
                    "dokon_name": dokon_names.dokon_name,
                    "hamyon": serializer_hamyon.data,
                    "mijoz_data": serializer.data,
                }
                return Response(data_Set)      
            return _user_test_views(request=request, phone=phone)


@extend_schema(
        request=ClientSerializers,
        responses= {
            202: UserDataUpdateSerialzier
        }
)
@api_view(['PUT'])
@permission_classes([DokonUserAuthentication])
def userData_update(request):
    if request.method =='PUT':
        user = request.user
        if user =='AnonymousUser':
            return Response({
                "errors": "user token requerid"
            })
        serializer = UserDataUpdateSerialzier(data=request.data)
        if serializer.is_valid():
            phone = serializer.data.get('phone')
            firt_name = serializer.data.get('firt_name')
            last_name = serializer.data.get('last_name')
            cashback_kard = serializer.data.get('cashback_kard') 
            random_status= serializer.data.get('random_status')
            UserData = User.objects.get(phone=phone)
            UserData.last_name = last_name
            UserData.first_name = firt_name
            UserData.save()
            hamyon = Hamyon.objects.get(id=phone)
            if hamyon.activete:
                pass
            else:
                kart = Kard.objects.create(
                    kard_cod = cashback_kard,
                    karta_random = random_status
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
              
            client_bool: bool = Klient.objects.filter(client_user__id=UserData.id).exists()
            if not(client_bool):
                client = Klient.objects.create(
                    client_name = firt_name,
                    mobile = phone,
                    client_user = UserData
                )
                client.save()
                all_shop = AllShop.objects.get(userId=user.id)
            
        
                all_shop.dokon_client.add(client)

                all_shop.save()
            else:
                client = Klient.objects.get(mobile=phone)
                client.client_name =f"{firt_name}  {last_name}"
                
            hamyon_seralizer = PostSerializer(hamyon)
            client_serialzier = ClientSerializers(client)
            data = {
                "hamyon": hamyon_seralizer.data,
                "client_data": client_serialzier.data
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors)
    

            


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cashback_user_update(request):
    if request.method =='PUT':
        user = request.user
        if user =='AnonymousUser':
            return Response({
                "errors": "user token requerid"
            })
        serializer = CashbackUserDataUpdateSerialzier(data=request.data)
        if serializer.is_valid():
            phone = user.phone
            firt_name = serializer.data.get('firt_name')
            last_name = serializer.data.get('last_name')
            cashback_kard = serializer.data.get('cashback_kard') 
            random_status= serializer.data.get('random_status')
            UserData = User.objects.get(phone=phone)
            UserData.last_name = last_name
            UserData.first_name = firt_name
            UserData.save()
            hamyon = Hamyon.objects.get(id=phone)
            if hamyon.activete:
                pass
            else:
                kart = Kard.objects.create(
                    kard_cod = cashback_kard,
                    karta_random = random_status
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
              
            client_bool: bool = Klient.objects.filter(client_user__id=user.id).exists()
            if not(client_bool):
                client = Klient.objects.create(
                    client_name = firt_name,
                    mobile = phone,
                    client_user = UserData
                )
                client.customer_type = True
                client.save()
              
            else:
                client = Klient.objects.get(mobile=phone)
                client.client_name =f"{firt_name}  {last_name}"
                
            hamyon_seralizer = PostSerializer(hamyon)
            client_serialzier = ClientSerializers(client)
            data = {
                "hamyon": hamyon_seralizer.data,
                "client_data": client_serialzier.data
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors)



















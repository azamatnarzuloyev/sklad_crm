from rest_framework.response import Response
from rest_framework import status, permissions
from cash.models import Hamyon
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from cash.serializers import PostSerializer
from .serializers import ClientSerializers, OtpSerializer
from account.models import PhoneOtp 
from account.send_otp import send_otp
# from permissions import IsSuperUser
from extensions.code_generator import get_client_ip
from magazin.models import Klient, AllShop
from account.models import User
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse


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
    return JsonResponse(res, status=status_code , safe=False)




class ClientVerifyOtp(APIView):


    permission_classes = [
        AllowAny,
    ]
    # throttle_scope = "verify_authentication"
    # throttle_classes = [
    #     ScopedRateThrottle,
    # ]
    @extend_schema (
            request=OtpSerializer,
            responses= {
                201: OtpSerializer
            }
    )
    def post(self, request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            user_token = request.user
            if str(user_token)=='AnonymousUser':
                return _errors_response(status_code=401, message='user not fount token required', detail=None)
            else:
                user_id = request.user.id
            received_code = serializer.data.get("code")
            # dokon_uuid = serializer.data.get('dokon_uuid')
            ip = get_client_ip(request)
            phone = cache.get(f"{ip}-for-authentication")
            telefon = phone
            otp = cache.get(phone)
            if otp is not None:
                if otp == received_code:
                    user, created = get_user_model().objects.get_or_create(phone=phone)
                    # user = User.objects.get(phone=phone)
                    # if user.two_step_password:
                    #     cache.set(f"{ip}-for-two-step-password", user, 250)
                    #     return _errors_response(status_code=200, message= {
                    #             "Thanks": "Please enter your two-step password",
                    #         }, detail=None)
                
        #   return Response({"data": "success"})
                    refresh = RefreshToken.for_user(user)
                    cache.delete(phone)
                    cache.delete(f"{ip}-for-authentication")

                    context = {
                        "created": created,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    phone = telefon
                    user_data =  User.objects.get(phone=phone)
                   
                    ism  = f"{user_data.first_name} {user_data.last_name}" and f"{user_data.first_name} {user_data.last_name}" or "AnonymousUser"
                   
                    hamyon_bool:bool = Hamyon.objects.filter(id=int(phone)).exists()
                    if hamyon_bool:
                        client_bool:bool = Klient.objects.filter(mobile=phone).values("mobile").exists()
                        if not(client_bool): 
                            klient = Klient.objects.create(
                            mobile = phone,
                            cashback_register = True,
                            foydalanuvchi_turi = 0,
                            client_name = ism,
                            client_user = user_data,)

                            klient.save()
                        klient = Klient.objects.get(mobile=phone)
                        dokon_user:bool = AllShop.objects.filter(userId__id=user_id).filter(dokon_client__id=klient.pk).exists()
                        if not(dokon_user):
                            shops = AllShop.objects.get(userId__id=user_id).dokon_client.add(klient)
                            shops.save()
                    else:
                        hamyon = Hamyon.objects.create(id=phone)
                        hamyon.save()
                        klient = Klient.objects.create(
                            mobile = phone,
                            cashback_register = True,
                            foydalanuvchi_turi = 0,
                            client_name = ism,
                            client_user = user_data,)

                        klient.save()
                    context = {
                            "created": created,
                            "client_id": klient.pk,
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        }
                    return _sesscess_respose(status_code=200 , data=context, register=False)
                    
                else:
                    return _errors_response(status_code=406 , message={  "Incorrect code.": "The code entered is incorrect."}, detail=None)
            else:
                return _errors_response(status_code=408, message={"Code expired.": "The entered code has expired."}, detail=None)
        else:
            return _errors_response(status_code=400, message=serializer.error_messages, detail=serializer.errors)
        
client_verify_view = ClientVerifyOtp.as_view()



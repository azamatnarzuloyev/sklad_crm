from functools import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status

# from account import send_otp
from account.serializers import (
    AuthenticationSerializer,
    MobileAuthenticationSerializers,
    OtpSerializer,
)
from extensions.code_generator import get_client_ip
from .models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from magazin.models import AllShop
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .send_otp import send_otp
from django.core.cache import cache


class MobileLoginViews(APIView):
    def post(self, request, format=None):
        """phone and shop_password"""
        serializer = MobileAuthenticationSerializers(data=request.data)
        if serializer.is_valid():
            received_phone = serializer.data.get("phone")
            shop_password = serializer.data.get("shop_password")
            user_is_exists: bool = (
                get_user_model()
                .objects.filter(phone=received_phone)
                .values("phone")
                .exists()
            )
            if user_is_exists:
                dokon_user = User.objects.get(phone=received_phone)
                if dokon_user.shop_password == shop_password or dokon_user.is_superuser:
                    return send_otp(
                        request,
                        phone=received_phone,
                    )
                return Response(
                    {
                        "data": None,
                        "errors": True,
                        "message": "User Dokon Foydalanuvchisi emas dokon userni kiriting",
                        "detail": "",
                    }
                )
            return Response(
                {
                    "data": None,
                    "errors": True,
                    "message": "phone not fount",
                    "detail": "telefon dokon userniki emas",
                }
            )

        return Response(
            {"data": None, "errors": True, "message": serializer.error_messages}
        )


class MobileDOkonVerifyOtp(APIView):
    """
    post:
        Send otp

    """

    # permission_classes = [
    #     AllowAny,
    # ]
    # throttle_scope = "verify_authentication"
    # throttle_classes = [
    #     ScopedRateThrottle,
    # ]

    def post(self, request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            two_step_passwords = serializer.data.get("two_step_passwords")
            received_code = serializer.data.get("code")
            ip = get_client_ip(request)
            phone = cache.get(f"{ip}-for-authentication")
            otp = cache.get(phone)

            if otp is not None:
                if otp == received_code:
                    user, created = get_user_model().objects.get_or_create(phone=phone)
                    # if user.two_step_password:
                    #     cache.set(f"{ip}-for-two-step-password", user, 250)
                    #     check_password: bool = user.check_password(two_step_passwords)
                    #     if check_password:
                    #         refresh = RefreshToken.for_user(user)
                    #         cache.delete(phone)
                    #         cache.delete(f"{ip}-for-authentication")

                    #         context = {
                    #             "created": created,
                    #             "refresh": str(refresh),
                    #             "access": str(refresh.access_token),
                    #         }
                    #         return Response(context)
                    #     return Response(
                    #         {
                    #             "Thanks": "Please enter your two-step password",
                    #         },
                    #         status=status.HTTP_200_OK,
                    #     )

                    refresh = RefreshToken.for_user(user)
                    cache.delete(phone)
                    cache.delete(f"{ip}-for-authentication")

                    context = {
                        "created": created,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }

                    return Response(
                        context,
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {
                            "Incorrect code.": "The code entered is incorrect.",
                        },
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            else:
                return Response(
                    {
                        "Code expired.": "The entered code has expired.",
                    },
                    status=status.HTTP_408_REQUEST_TIMEOUT,
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import APIView
from .serializers import DokonAuthenticationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class DokonRegister(APIView):
    """
    post:
        Send mobile number for Register.
        parameters: [phone,]
    """

    # throttle_scope = "authentication"
    # throttle_classes = [
    #     ScopedRateThrottle,
    # ]
    def post(self, request):
        serializer = DokonAuthenticationSerializer(data=request.data)
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
                return Response(
                    {
                        "User exists.": "Please enter a different phone number.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # The otp code is sent to the user's phone number for authentication
            else:
                user, created = get_user_model().objects.get_or_create(
                    phone=received_phone, shop_password=shop_password, vendor_user=True
                )
                refresh = RefreshToken.for_user(user)

                context = {
                    "created": created,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
                return Response(context, status=status.HTTP_201_CREATED)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class DokonLogin(APIView):
    """
    post:
       login dokon phone and passwords
    """

    def post(self, request):

        serializer = DokonAuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            received_phone = serializer.data.get("phone")
            shop_password = serializer.data.get("shop_password")

            user_is_exists: bool = (
                get_user_model()
                .objects.filter(phone=received_phone)
                .values("phone")
                .exists()
            )
            if not user_is_exists:
                return Response(
                    {
                        "No User exists.": "Please enter another phone number.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # The otp code is sent to the user's phone number for authentication
            else:
                try:
                    user, created = get_user_model().objects.get_or_create(
                        phone=received_phone, shop_password=shop_password
                    )
                    refresh = RefreshToken.for_user(user)

                    context = {
                        "created": created,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    return Response(context, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({"errors": "phone or password errors"})

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

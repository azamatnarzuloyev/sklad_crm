from permission.permissions import  IsSuperUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .models import Address , User
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from cash.models import Hamyon
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UsersListSerializer,
    UserDetailUpdateDeleteSerializer,
    UserProfileSerializer,
    AuthenticationSerializer,
    OtpSerializer,
    ChangeTwoStepPasswordSerializer,
    CreateTwoStepPasswordSerializer,
    AddressSerializer,
)
from .models import PhoneOtp 
from .send_otp import send_otp
# from permissions import IsSuperUser
from extensions.code_generator import get_client_ip



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT,content_type="status seksesfull")
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, content_type="status error")


class AddressCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def post(self, request):
        address = Address.objects.filter(user=self.request.user)
        if address.exists():
            return Response({"error": "You already have an address. Edit it"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressUpdateView(RetrieveUpdateAPIView):
    '''
    Retrieve or Update Address details by User ID.
    '''
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    lookup_field = 'user'

class UsersList(ListAPIView):
    """
    get:
        Returns a list of all existing users.
    """

    serializer_class = UsersListSerializer
    # permission_classes =  IsSuperUser,
    
    filterset_fields = [
        'phone',
    ]


    def get_queryset(self):
        return get_user_model().objects.all()


class UsersDetailUpdateDelete(RetrieveUpdateDestroyAPIView):


    serializer_class = UserDetailUpdateDeleteSerializer
    permission_classes = [
        permissions.IsAdminUser
    ]

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(get_user_model(), pk=pk)


class UserProfile(RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the profile of user.
    put:
        Update the detail of a user instance
        parameters: exclude[password,]
    delete:
        Delete user account.
        
        parameters: [pk]
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated,]
 
    # throttle_scope = "authentication"
    # throttle_classes = [
    #     ScopedRateThrottle,
    # ]

    def get_object(self):
        return self.request.user




class Login(APIView):
    """
    post:
        Send mobile number for Login.
        parameters: [phone,]
    """

    permission_classes = [
        AllowAny,
    ]
    throttle_scope = "authentication"
    throttle_classes = [
        ScopedRateThrottle,
    ]

    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            received_phone = serializer.data.get("phone")

            user_is_exists: bool = User.objects.filter(phone=received_phone).values("phone").exists()
            if not user_is_exists:
                return Response(
                    {
                        "No User exists.": "Please enter another phone number.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # The otp code is sent to the user's phone number for authentication
            return send_otp(
                request,
                phone=received_phone,
            )

        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST,
            )
        




class Register(APIView):
    """
    post:
        Send mobile number for Register.
        parameters: [phone,]
    """

    permission_classes = [
        AllowAny,
    ]
    # throttle_scope = "authentication"
    # throttle_classes = [
    #     ScopedRateThrottle,
    # ]

    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            received_phone = serializer.data.get("phone")
 
            user_is_exists: bool = get_user_model().objects.filter(phone=received_phone).values("phone").exists()
            if user_is_exists:
                return send_otp(
                    request,
                    phone=received_phone,
            )
            # The otp code is sent to the user's phone number for authentication
            return send_otp(
                request,
                phone=received_phone,
            )

        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST,               
            )

            
class VerifyOtp(APIView):
    """
    post:
        Send otp code to verify mobile number and complete authentication.
        parameters: [otp,]
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
                    if user.two_step_password:
                        cache.set(f"{ip}-for-two-step-password", user, 250)
                        check_password: bool = user.check_password(two_step_passwords)
                        if check_password:
                            refresh = RefreshToken.for_user(user)
                            cache.delete(phone)
                            cache.delete(f"{ip}-for-authentication")

                            context = {
                                "created": created,
                                "refresh": str(refresh),
                                "access": str(refresh.access_token),
                            }
                            return Response(context)
                        return Response(
                            {
                                "Thanks": "Please enter your two-step password",
                            },
                            status=status.HTTP_200_OK,
                        )

                    refresh = RefreshToken.for_user(user)
                    cache.delete(phone)
                    cache.delete(f"{ip}-for-authentication")

                    context = {
                        "created": created,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    # if created:
                    #     datase = Hamyon.objects.create(id=phone)
                    #     datase.save()
                     
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






class CreateTwoStepPassword(APIView):
    """
    post:
        Send a password to create a two-step-password.
        
        parameters: [new_password, confirm_new_password]
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        if request.user.two_step_password:
            return Response({"Error!": "Your request could not be approved."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CreateTwoStepPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.data.get("new_password")
        try:
            _: None = validate_password(new_password)
        except ValidationError as err:
            return Response({"errors": err}, status=status.HTTP_401_UNAUTHORIZED)
        user = get_object_or_404(get_user_model(), pk=request.user.pk)
        user.set_password(new_password)
        user.two_step_password = True
        user.save(update_fields=["password", "two_step_password"])
        return Response({"Successful.": "Your password was changed successfully."}, status=status.HTTP_200_OK)



class ChangeTwoStepPassword(APIView):
    """
    post:
        Send a password to change a two-step-password.
        
        parameters: [old_password, new_password, confirm_new_password,]
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        if request.user.two_step_password:
            serializer = ChangeTwoStepPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            new_password = serializer.data.get("new_password")

            try:
                _: None = validate_password(new_password)
            except ValidationError as err:
                return Response(
                    {"errors":err},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            old_password = serializer.data.get("old_password")
            user = get_object_or_404(get_user_model(), pk=request.user.pk)
            check_password: bool = user.check_password(old_password)
            if check_password:
                user.set_password(new_password)
                user.save(update_fields=["password"])

                return Response(
                    {
                        "Successful.":"Your password was changed successfully.",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "Error!":"The password entered is incorrect.",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        return Response(
            {
                "Error!":"Your request could not be approved.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
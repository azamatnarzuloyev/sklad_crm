from rest_framework.response import Response
from .models import AllShop
from .serializers import DokonCreateSerializer, AllShopSerializers, DokonLoginSerialzier
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from product.models import Product
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User
from django.http import JsonResponse


class DokonCreateView(APIView):
    # permission_classes = [DokonUserAuthentication]
    def post(self, request, format=None):
        serializer = DokonCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                ism = serializer.data.get("foydalanuvchi_ism")
                telefon = serializer.data.get("phone")
                familya = serializer.data.get("foydalanuvchi_familya")
                password = serializer.data.get("password")
                shop_name = serializer.data.get("shop_name")
                shop_password = serializer.data.get("shop_password")
                vendor = serializer.data.get("vendor")
                sklad = serializer.data.get("sklad")

                user, created = get_user_model().objects.get_or_create(
                    phone=telefon, shop_password=password
                )
                dokon = AllShop.objects.create(
                    vendor=vendor,
                    foydalanuvchi_ism=ism,
                    foydalanuvchi_familya=familya,
                    dokon_name=shop_name,
                    userId=user,
                    passwords=shop_password,
                    sklad=sklad,
                )
                dokon.save()
                productCount = Product.objects.count()
                if productCount > 0 and not(vendor):
                    for product in Product.objects.all():
                        if product.serenaTrue_countFalse:
                            create_data = {
                                "id": f"{dokon.id}",
                                "store_name": f"{dokon.dokon_name}",
                                "product_count": None,
                                "vendor": False,
                                "sklad": dokon.sklad,
                                "array_serena": [],
                            }
                        else:
                            create_data = {
                                "id": f"{dokon.id}",
                                "store_name": f"{dokon.dokon_name}",
                                "product_count": 0,
                                "vendor": False,
                                "sklad": dokon.sklad,
                                "array_serena": None,
                            }
                        product.dokon_tavarlar.append(create_data)
                        product.save()
                serialzier = AllShopSerializers(dokon, many=False)
                return JsonResponse(
                    {"data": serialzier.data, "errors": False, "message": ""},
                    safe=False,
                )
            except Exception as e:
                return JsonResponse({"data": None, "errors": True, "message": f"{e}"})

        return JsonResponse(
            {"data": None, "errors": False, "message": serializer.errors}, safe=False
        )


def _dokon_login_funtions(phone, shop_passwords):
    user = User.objects.get(phone=phone, shop_password=shop_passwords)
    refresh = RefreshToken.for_user(user)
    context = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return context


class DokonLogin(APIView):
    def get(self, request, userId, format=None):
        dokons = AllShop.objects.get(userId=userId)
        serializer = AllShopSerializers(dokons, many=False)
        return Response(serializer.data)

    def post(self, request):
        serializer = DokonLoginSerialzier(data=request.data)
        if serializer.is_valid():
            telefon = serializer.data.get("phone")
            password = serializer.data.get("password")
            shop_passwords = serializer.data.get("shop_passwords", None)
            user_bool: bool = (
                User.objects.filter(phone=telefon, shop_password=password)
                .values("phone")
                .exists()
            )
            if user_bool and shop_passwords is None:
                userId = User.objects.get(phone=telefon)
                dokon_name = AllShop.objects.get(userId__id=userId.pk)
                return JsonResponse(
                    {
                        "data": {
                            "dokonName": dokon_name.dokon_name,
                            "user_name": dokon_name.foydalanuvchi_ism,
                            "user_id": userId.pk,
                            "message": "Dokon parolini kriting",
                        },
                        "errors": False,
                        "message": "",
                    },
                    safe=False,
                )
            if user_bool and shop_passwords is not None:
                userId = User.objects.get(phone=telefon)
                dokon = AllShop.objects.get(userId=userId)
                if str(dokon.passwords) == str(shop_passwords):
                    user_data = _dokon_login_funtions(
                        phone=telefon, shop_passwords=password
                    )
                    dokon_nameData = dokon.dokon_name
                    dokonSerialzier = AllShopSerializers(dokon, many=False)
                    data = {
                        "dokon_name": dokon_nameData,
                        "user": dokonSerialzier.data,
                        "refresh": user_data["refresh"],
                        "access": user_data["access"],
                    }
                    return JsonResponse(
                        {"data": data, "errors": False, "message": ""}, safe=False
                    )
                else:
                    return JsonResponse(
                        {"data": None, "errors": True, "message": "dokon paroli xato"},
                        safe=False,
                    )
        return JsonResponse(
            {"data": "", "errors": True, "message": DokonLoginSerialzier.errors},
            safe=False,
        )


class DokonlistVIew(APIView):
    # permission_classes = [DokonUserAuthentication]
    def get(self, request, userId=None, format=None):
        if userId:
            dokons = AllShop.objects.get(userId=userId)
            serializer = AllShopSerializers(dokons)
        else:
            dokon = AllShop.objects.all()
            serializer = AllShopSerializers(dokon, many=True)

        return Response(serializer.data)

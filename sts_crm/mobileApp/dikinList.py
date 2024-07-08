from magazin.models import AllShop
from rest_framework import status
from rest_framework.decorators import api_view , permission_classes
from magazin.serializers import AllShopSerializers
from account.models import User
from permission.permissions import DokonUserAuthentication
from django.http import JsonResponse

@api_view(['GET'])
@permission_classes([DokonUserAuthentication])
def allshop_user_funtion(request):
    if request.method =='GET':
        user = request.user
        user_bool:bool = User.objects.filter(id=user.id).exists()
        if user_bool:
            user_ids = User.objects.get(id=user.id)
            if user_ids.is_superuser:
                dokon = AllShop.objects.all()
                serialzier = AllShopSerializers(dokon , many=True)
                return JsonResponse(
                    {
                        "data": serialzier.data,
                        "errors": False,
                        "message": ""
                    }
                )
            if user_ids.vendor_user:
                dokon = AllShop.objects.get(userId__id=user.id)
                dokon_serialzier=  AllShopSerializers(dokon , many=False)
                return JsonResponse(
                    {
                        "data": dokon_serialzier.data,
                        "errors": False,
                        "message": ""
                    }
                )
        return JsonResponse({
            "data": None,
            "errors": True,
            "message": "user not fount"
        })
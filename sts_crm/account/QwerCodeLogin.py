"""
toke_uuid : char (200),
user_uuid: []
islogginId: flase 
divase: [],
sessin: ""
create_at: date
crate_time: datetime
update_date: update_datetime
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User , GouseUser
from rest_framework_simplejwt.tokens import RefreshToken
from magazin.models import AllShop
from magazin.serializers import AllShopSerializers
from .serializers import DeviseSerialzier


class GoustUserViews(APIView):
    def get(self, request , uuid_token=None , format=None):
        name = request.GET.get('name')
        host = request.GET.get('host')
        model = request.GET.get('model')

        if uuid_token is not None:
            gost_user:bool = GouseUser.objects.filter(token_uuid=uuid_token).exists()
            if gost_user:
                user_token = GouseUser.objects.get(token_uuid=uuid_token)
                if user_token.islogginIn:
                    user = User.objects.get(id=user_token.userId)
                    refresh = RefreshToken.for_user(user)
                    all_shop = AllShop.objects.get(userId=user_token.userId)
                    serialzier = AllShopSerializers(all_shop, many=False)
                    data_set=  {
                        "dokon_name": all_shop.dokon_name,
                        "user": serialzier.data,
                        "islogginIn":True,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        
                    }
                    content = {
                        "islogginIn":True,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),

                    }
                    return Response(data=data_set)
         
                else:
                    return Response({
                        "islogginIn": False,
                        "data": None,
                    })
            if not(gost_user):
                gost_users = GouseUser()
                gost_users.token_uuid = uuid_token
                gost_users.name = name
                gost_users.hostName = host
                gost_users.model = model
                gost_users.save()
                return Response({
                        "islogginIn": False,
                        "data": None,
                    })

 
    def post(self, request, uuid_token=None,  format=None):

        # user =  request.user 
        # if str(user) == "AnonymousUser":
        #     return Response(
        #         {
        #             "data": None,
        #             "errors": True,
        #             "message": "user not fount"
        #         }
        #     )
        id = request.data.get('id')
        if uuid_token is not None:
            gost_bool :bool = GouseUser.objects.filter(token_uuid=uuid_token).exists()
            if gost_bool:
                gost_data = GouseUser.objects.get(token_uuid=uuid_token)
                gost_data.userId = int(id)
                gost_data.islogginIn = True
                gost_data.save()

                return Response({
                    "status": True,
                    "errors": False,
                    "message": ""

                })
        
            return Response({
                "status": False,
                "errors": True,
                "message": "Not fount",
            })        

        return Response({
              "status": False,
                "errors": True,
                "message": "token_uuid required",
        })
       

class DiveViews(APIView):
    def get(self, request, pk=None):
        user = User.objects.get(id=pk)
        serialzier = DeviseSerialzier(user)
        return Response(
            serialzier.data
        )

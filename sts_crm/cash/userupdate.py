from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.models import User
from cash.models import DepozitCarddata, Hamyon, Kard
from cash.serializers import PostSerializer
from magazin.models import Klient
from savdo.news_savdo import otp_generators
from savdo.serializers import CashbackUserDataUpdateSerialzier, ClientSerializers
from rest_framework import status


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
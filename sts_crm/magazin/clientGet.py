from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Klient
from cash.models import Hamyon
from cash.serializers import PostSerializer
from account.models import User
from .serializers import CLientFilterPhoneSerialzier, KlientSerialzier
from drf_spectacular.utils import extend_schema


@api_view(['GET'])
def client_get(request):
    if request.method =='GET':
        client = Klient.objects.all()
        user = User.objects.all()
        clientSerialzier = KlientSerialzier(client, many=True)
        user_data = []
        for i in user:
            arr = {
                "id" : i.id,
                "phone": i.phone,
                "first_name": i.first_name,
                "last_name": i.last_name,
            }
            user_data.append(arr)
        data = {
            "client_user": clientSerialzier.data,
            "all_user": user_data

        }
   
        return Response(data, status=status.HTTP_200_OK)
    

@extend_schema(
        request= CLientFilterPhoneSerialzier,
        responses= {
            200: PostSerializer,
        }
    )
@api_view(['POST'])
def hamfonFilter(request):
    if request.method =='POST':
        phoneSerialzier  = CLientFilterPhoneSerialzier(data=request.data)
        if phoneSerialzier.is_valid():
            phone = phoneSerialzier.data.get('phone')
            hamyon = Hamyon.objects.get(id=phone)
            serializer =PostSerializer(hamyon)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(phoneSerialzier.errors) 
    

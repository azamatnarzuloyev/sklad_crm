from rest_framework.response import Response

from rest_framework.decorators import api_view , permission_classes
from permission.permissions import DokonUserAuthentication, DokonUserSHopAuthentication

from savdo.models import TechnicalStaff , InstallationService

from savdo.serializers import TechnicalStafSerializer , InstallationServiceSerialzier

from rest_framework import status

from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([DokonUserAuthentication])
def ustanofka_xodimlar(request, pk=None):
    """ ustanofka xodimlar to'liq ko'rish """
    if pk is not None:
        technical = TechnicalStaff.objects.get(id=pk)
        serializer = TechnicalStafSerializer(technical)
    else:
        technical = TechnicalStaff.objects.all()
        serializer = TechnicalStafSerializer(technical, many=True)
    if request.method =='GET':
        return Response(serializer.data)
    
    if request.method =='POST':
        serializers = TechnicalStafSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save() 
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors)
    
    if request.method =='PUT':
        technical_serialzier = TechnicalStafSerializer(technical, data=request.data)
        if technical_serialzier.is_valid():
            technical_serialzier.save()
            return Response(technical_serialzier.data)
        return Response(technical_serialzier.errors)
    
    if request.method =='DELETE':
         technical.delete()
         return Response({
             "delete": "successful"
         })
      


@api_view(['GET', 'POST' , 'PUT', 'DELETE'])
@permission_classes([DokonUserAuthentication])
def servis_funtion(request, pk=None):
    """ yangi ustanofkachilar uchun xizmat yaratish va xizmatchilarni qo'shish """
    if request.method =='GET':
        if pk is not None:
            servis = InstallationService.objects.get(id=pk)
            serializer = InstallationServiceSerialzier(servis)
            return Response(serializer.data)
        servis = InstallationService.objects.all()
        serializer = InstallationServiceSerialzier(servis, many=True)
        return Response(serializer.data)
    
    if request.method =='POST':
        servisserializer = InstallationServiceSerialzier(data=request.data)
        if servisserializer.is_valid():
            servisserializer.save()
            return Response(servisserializer.data)
        return Response(servisserializer.errors)


    if request.method =='PUT':
        if pk is not None:
            servisses = InstallationService.objects.get(id=pk)
            serializers = InstallationServiceSerialzier(servisses, data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data)
            return Response(serializers.errors)
        return Response({
            "pk": "is not none"
        })
    if request.method =="DELETE":
        if pk is not None:
            servises = InstallationService.objects.get(id=pk)
            if servises.status_servis:
                return Response({
                    "errors": "status servis true you can't delete this"
                })
            servises.delete()
            return Response({
                "delete" : "successful"
            })
        return Response ({
            "pk":  "is not fount"
        })
    


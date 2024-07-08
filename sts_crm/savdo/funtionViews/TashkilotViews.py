from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from magazin.models import TashkilotYaratish
from magazin.serializers import TashkilotSerializers
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from permission.permissions import DokonUserAuthentication


@extend_schema(
    request=TashkilotSerializers,
    responses={
        200: TashkilotSerializers,
        201: TashkilotSerializers,
        202: TashkilotSerializers,
    },
)
@api_view(["GET", "POST"])
@permission_classes([DokonUserAuthentication])
def tashkilot_funtion(request, pk=None):
    if request.method == "GET":
        if pk is not None:
            tashkilot = TashkilotYaratish.objects.get(id=pk)
            tashkilot_serialzier = TashkilotSerializers(tashkilot, many=True)
            return Response(tashkilot_serialzier.data, status=status.HTTP_200_OK)
        tashkilot = TashkilotYaratish.objects.all()
        serialzier = TashkilotSerializers(tashkilot, many=True)
        return Response(serialzier.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        tashkilot_serialziers = TashkilotSerializers(data=request.data)
        if tashkilot_serialziers.is_valid(raise_exception=True):
            inn_raqam = tashkilot_serialziers.data.get("inn_raqam")
            if TashkilotYaratish.objects.filter(inn_raqam=inn_raqam).exists():
                return Response({"errors": "Kompanya all ready exists"})

            tashkilot_serialziers.save()
            return Response(tashkilot_serialziers.data)
        return Response(tashkilot_serialziers.errors)

    if request.method == "PUT":
        tashkilot_data = TashkilotYaratish.objects.get(id=pk)
        serialzier_data = TashkilotSerializers(tashkilot_data, data=request.data)
        if serialzier_data.is_valid():
            serialzier_data.save()
            return Response(serialzier_data.data, status=status.HTTP_201_CREATED)
        return Response(serialzier_data.errors)
    if request.method == "DELETE":
        tash = TashkilotYaratish.objects.get(id=pk)
        tash.delete()
        return Response(
            {
                "delete": "success",
            },
            status=status.HTTP_204_NO_CONTENT,
        )

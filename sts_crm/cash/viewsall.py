from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Kard, Hamyon
from .serializers import PostSerializer, KartSerializer
from rest_framework.permissions import IsAuthenticated




class KardListUpdateViews(generics.ListAPIView):
    queryset = Kard.objects.all()
    serializer_class = KartSerializer
    lookup_field ="pk"


class KartListRetriveupdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Kard.objects.all()
    serializer_class = KartSerializer
    lookup_field ="pk"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([permissions.IsAuthenticated])
def hamyon_get_or_update(request, pk):
    hamyon = get_object_or_404(Hamyon, id=pk)
    if request.method == "GET":
        hamyon_serializers = PostSerializer(hamyon)
        return Response(hamyon_serializers.data, status=status.HTTP_200_OK)


def _get_hamyon(pk=None):
    """
      kard get id 
    """
    try:
        return Hamyon.objects.get(id=pk)
    except Hamyon.DoesNotExist:
        raise NotFound()




@api_view(['GET'])
def get_hamyon(request, pk=None):
    hamyon = _get_hamyon(pk=pk)
    serializer = PostSerializer(hamyon)

    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_hamyon(request, pk=None):
    hamyon = _get_hamyon(pk=pk)

    serializer = PostSerializer(hamyon, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    kard = []

    for kard_id in request.data.get('kard') or []:
        try:
            tag = Kard.objects.get(id=kard_id)
            kard.append(tag)
        except Kard.DoesNotExist:
            raise NotFound()
    if kard:
      hamyon.kard.set(kard)
      return Response(data=serializer.data, status=status.HTTP_200_OK)

    else:
        kard = None
        return Response({"errors": "karta not fount"})
    


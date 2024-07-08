from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Istoriya
from .serializers import IstoriyaSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import posttast
from django.views.decorators.cache import cache_page
from product.models import Product
from product.serializers import ProductSerializer
from .tasks import posttast

class ListPostviews(ListAPIView):
        queryset = Istoriya.objects.all()
        serializer_class = IstoriyaSerializers


    

@cache_page(timeout=60 * 30)  # cache for 30 minutes
def home_cache(request):
 
    return render(
          request,
          "report.html"  
    )


@api_view(['GET'])
def post_tasks(request):
      posttast.delay()
      return Response({"data":"success"})



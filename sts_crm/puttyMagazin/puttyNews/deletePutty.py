from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.response import Response
from puttyMagazin.models import TavarPutty , DokonPutty
from product.models import Product
from magazin.models import AllShop
from .serialzier import PuttyDeleteSerializer
from drf_spectacular.utils import extend_schema
from utills.productupdate import VendorProductsUpdate , ProductUpdate
     


class DeletePuttyViews(APIView):
    @extend_schema(
        request=PuttyDeleteSerializer,
        responses={204: PuttyDeleteSerializer}
    ) 
    def delete(self, request, format=None):
        serializer = PuttyDeleteSerializer(data=request.data)
        if serializer.is_valid():
            putty_id = serializer.data.get('putty_id')
            putty = TavarPutty.objects.get(id=putty_id)
            shop_id = putty.shopId
            if putty.putty_status:
                return Response({"data":None, "errors":True, "message": "putty is not delete"})
            else:
                dokon = AllShop.objects.get(id=putty.shopId.id)
                if dokon.vendor:
                    vendor_prod = VendorProductsUpdate(products=putty.tavarlar , shop_id=shop_id) 
                    vendor_prod.product__append
                else:
                    dokon_prod = ProductUpdate(products=putty.tavarlar , shop_id=shop_id)
                    dokon_prod.append_product
                putty.delete()
            return Response({"data": "success", "errors": False, "message": ""})
                   
        return Response({"data": None, "errors": True, "message": serializer.errors})
                           
                          
                     

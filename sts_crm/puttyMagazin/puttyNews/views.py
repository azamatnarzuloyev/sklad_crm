from rest_framework.response import Response
from puttyMagazin.models import TavarPutty , DokonPutty , ZakasProduct
from .serialzier import GetPuttySerialzier, GetTestPuttySerialzier, PostPuttyProductSerializer, GetTavarPuttySerialzier, VendorProductSerializer, VendorTavarlar
from rest_framework import status
from rest_framework.views import APIView
from magazin.models import AllShop
from django.utils import timezone
from product.models import Product
from rest_framework.generics import ListAPIView, ListCreateAPIView
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse
from permission.permissions import DokonUserAuthentication
from rest_framework.request import Request
from utills.productupdate import VendorProductsUpdate , ProductUpdate



class TavarPuttyApiviews(APIView):
    # permission_classes = [DokonUserAuthentication]
    @extend_schema(
        request=GetTavarPuttySerialzier,
        responses={200: GetTavarPuttySerialzier,
                 },
        ) 
    def get(self, request):
        putty = TavarPutty.objects.all()
        serializer = GetTavarPuttySerialzier(putty, many=True)
        return Response(data=serializer.data,  status=status.HTTP_200_OK)
    @extend_schema(
        request=GetTavarPuttySerialzier,
        responses={
                   201: PostPuttyProductSerializer},
        ) 
    def post(self, request:Request):
        # user =  request.user 
        # if str(user) == "AnonymousUser":
        #     data = {
        #         "data": None,
        #         "errors": True,
        #         "message": "Token not valid"
        #     }
        #     return JsonResponse(data=data , safe=False)
        serializer = PostPuttyProductSerializer(data=request.data)
        if serializer.is_valid():
            error_prod = []
            tavarlar = serializer.data.get('tavarlar')
            shop_id = serializer.data.get('shop_id')
            send_maagzinId = serializer.data.get('send_maagzinId')
            comentary = serializer.data.get('comentary')
            zakasproductstatus=  serializer.data.get('zakasproductstatus')
            dokon = AllShop.objects.get(id=shop_id)   
            vendor = dokon.vendor
            if vendor:
                putty_bool:bool = DokonPutty.objects.filter(dokon_uuid__id=dokon.id).exists()
                if not(putty_bool):
                    putty_create = DokonPutty.objects.create(dokon_uuid=dokon)
                    putty_create.save()
                product_product = VendorProductsUpdate(products=tavarlar, shop_id=dokon.pk)
                test_product = product_product.product_test_remove
                if len(test_product) > 0:

                    return JsonResponse({"data": None, "errors": True, "message": test_product}, safe=False)  
            else:
                product_product = ProductUpdate(products=tavarlar , shop_id=dokon.pk)
                test_prod =  product_product.test_product_remove
                if len(test_prod) > 0:
                    return JsonResponse({"data": None, "errors": True, "message": test_prod}, safe=False)  
            putty = TavarPutty.objects.create(
                shopId = dokon,
                tavarlar = tavarlar,
                send_maagzinId = send_maagzinId,
                create_date = timezone.now(),
                comentary = comentary,
                zakasproductstatus = zakasproductstatus
            )
            putty.save()

            res_data = {
                "id": putty.id,
                "shopId": shop_id,
                "create_date": putty.create_date,
                "tavarlar": putty.tavarlar,
                "send_maagzinId": putty.send_maagzinId
            }
            if zakasproductstatus is not None:
                zakas_product = ZakasProduct.objects.get(id=zakasproductstatus)
                for i in tavarlar:
                    for j in zakas_product.products:
                        if i.get('id') == j.get('product_id'):
                            if i.get('product_serena') is not None:
                                j['yuborilgan_count'] = len(i.get('product_serena'))
                                j['status'] =True
                                zakas_product.save()
                            else:
                                j['yuborilgan_count'] = i.get('product_count')
                                j['status'] = True
                                zakas_product.save()
            if vendor:
                product_product = VendorProductsUpdate(products=tavarlar, shop_id=dokon.pk).remove_product
                
            else:
                product_product = ProductUpdate(products=tavarlar , shop_id=dokon.pk).remove_product
            
            return JsonResponse(res_data , safe=False)

            
    

class TavarPuttyDetailApiviews(APIView):

    @extend_schema(
        request=GetTavarPuttySerialzier,
        responses={200: GetTavarPuttySerialzier,
                },
        ) 
    def get(self, request, pk):
        try:
            putty = TavarPutty.objects.get(id=pk)
            serializer = GetTavarPuttySerialzier(putty)
            return Response(data=serializer.data,  status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors": f"{e}"}, status=status.HTTP_404_NOT_FOUND)





class VendorProductViews(ListAPIView):
    queryset = DokonPutty.objects.all()
    serializer_class = VendorTavarlar
    lookup_field = "pk"


class PuttyViews(ListCreateAPIView):
    queryset = TavarPutty.objects.all()
    serializer_class = GetTavarPuttySerialzier
    lookup_field ="pk"


class DokonPuttyGet(APIView):
    """ 
    putty get request 
    agar user mavjud bo'lmasa 
    shop_id required 
    agar user token bo'lsa shart emas
    
    """
    @extend_schema(
        parameters= [
            GetTestPuttySerialzier
        ],
        request=GetTestPuttySerialzier,
        responses={200: GetTavarPuttySerialzier}
    ) 
    def get(self, request):
        serializer = GetPuttySerialzier(data=request.data)
        if serializer.is_valid():
            shop_id = serializer.data.get('shop_id')
            putty_status= serializer.data.get('putty_status')
            send_maagzinId = serializer.data.get('send_maagzinId')
            sendMagazinIdToken = serializer.data.get('sendMagazinIdToken')
            user = request.user
            if str(user) == "AnonymousUser":
                if shop_id is not None:
                    putty_id = TavarPutty.objects.filter(shopId__id=shop_id, putty_status=putty_status)
                    # if len(putty_id) > 1:
                    serializer = GetTavarPuttySerialzier(putty_id, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
        
                if send_maagzinId is not None:
                    putty_id = TavarPutty.objects.filter(send_maagzinId=send_maagzinId, putty_status=putty_status)
                    serializer = GetTavarPuttySerialzier(putty_id, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            if user.id is not None:
                if sendMagazinIdToken:
                    user_id = user.id
                    all_shop = AllShop.objects.get(userId__id = user_id)
                    putty_id = TavarPutty.objects.filter(send_maagzinId=all_shop.id, putty_status=putty_status)
                else:
                    user_id = user.id
                    all_shop = AllShop.objects.get(userId__id = user_id)
                    putty_id = TavarPutty.objects.filter(shopId__id=all_shop.id, putty_status=putty_status) 
                
         
                serializer = GetTavarPuttySerialzier(putty_id, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
       
            return Response({"data": "not fount"}, status=status.HTTP_204_NO_CONTENT)        
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)
    



    



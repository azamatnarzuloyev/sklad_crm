from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from puttyMagazin.serialziers import ZakasProductSerializers , ProductZakasSerializers
from puttyMagazin.models import ZakasProduct
from magazin.models import AllShop
from rest_framework.request import Request
from permission.permissions import DokonUserAuthentication
from datetime import date 
from drf_spectacular.utils import extend_schema
import random



def _error_data(status_code , message , detail):
    data = {     
                "data": None,
                "errors": True,
                "status": 200,
                "status_code": status_code,
                "message": message,
                "detail": detail,
                "token": "",
            },
    return Response(data, status=status_code)


def _success_data(status_code , data):
    data_set = {     
                "data": data,
                "errors": False,
                "status": 200,
                "status_code": status_code,
                "message": "",
                "detail": "",
                "token": "",
        },


    return Response(data_set, status=status_code )


@extend_schema(
        request=ProductZakasSerializers ,
        responses= {201: ZakasProductSerializers, 200: ZakasProductSerializers},
)
@api_view(['POST', 'GET' , 'PUT', 'DELETE'])
@permission_classes([DokonUserAuthentication])
def zakasProduct_funtion(request:Request):
    if request.method =='POST':
        """ yangi zakas yaratish """
        
        product_data = []
        # if request.data.get('products') is None:
        #     return _error_data(status_code=400, message="product=None ega bo'lolmaydi ", detail=None)
        # for i in request.data.get('products'):
        #     prod_serialzier = ProductZakasSerializers(data=i, many=False)
        #     if prod_serialzier.is_valid():
        #         product_data.append(i)
        #     else:
        #         return _error_data(status_code=400 , message=prod_serialzier.error_messages , detail=prod_serialzier.errors)

        # request.data['products'] = product_data
        if request.data['products'] is not None:
            for i in request.data['products']:
                if i.get('product_id') is not None and i.get('product_name') is not None  and i.get('product_count') is not None:
                    arr = {
                        "product_id": i['product_id'],
                        "product_name": i['product_name'],
                        "product_count": i['product_count'],
                        "status": False,
                        "yuborilgan_count": 0,
                        "return_bool": False
                    }
                    product_data.append(arr)
                else:
                    return Response({
                        "status_code": 400 , 
                        "message": "malumot xato kiritilgan" , 
                        "detail": {
                         "product_id": "",
                        "product_name": "",
                        "product_count": "",
                        "status": False,
                        "yuborilgan_count": 0,
                        "return_bool": False
                    }
                    })
        else:
            return _error_data(status_code=400, message="products is not None" , detail="")
        request.data['products']= product_data
        nomer_zakas = random.randint(10000, 99999)
        request.data['nomer_zakas'] =nomer_zakas
        serialzier = ZakasProductSerializers(data=request.data)
        if serialzier.is_valid():
            serialzier.save()
            return _success_data(status_code=201, data=serialzier.data)
        return _error_data(status_code=400, message=serialzier.error_messages , detail=serialzier.errors)

            
    if request.method =='GET':
        """ zakaslarni ko'rish har bir do'kon uchun alohida faqat skladga hammasi ko'rinadi """
        user = request.user 
        # shop_id = request.data.get('shop_id')
        # all_shop = AllShop.objects.get(id=shop_id)
        all_shop = AllShop.objects.get(userId__id=user.id)
        date_today = request.data.get('date_today', None)
        if all_shop.sklad:
         
            if date_today is None:
                zakas_product = ZakasProduct.objects.filter(qabul=False).order_by('-create_at')
                serialziers = ZakasProductSerializers(zakas_product, many=True)
                return _success_data(status_code=200, data=serialziers.data)
            else:
                zakas_product = ZakasProduct.objects.filter(date_filter=date_today).order_by('-create_at')
                serialziers = ZakasProductSerializers(zakas_product, many=True)
                return _success_data(status_code=200, data=serialziers.data)

        else:
            if date_today is None:
                zakas_product = ZakasProduct.objects.filter(shop_id=str(all_shop.id)).order_by('-create_at')
                serialzierss = ZakasProductSerializers(zakas_product, many=True)
                return _success_data(status_code=200, data=serialzierss.data)
            else:
                zakas_product = ZakasProduct.objects.filter(date_filter=date_today, shop_id=str(all_shop.id)).order_by('-create_at')
                serialzierss = ZakasProductSerializers(zakas_product, many=True)
                return _success_data(status_code=200, data=serialzierss.data)



    if request.method == 'PUT':
        "zakaslarni update qilish "
        zakas_id = request.data.get('zakas_id')
        if zakas_id is not None:
            zakas_data = ZakasProduct.objects.get(id=zakas_id)
            serializers = ZakasProductSerializers(zakas_data , data=request.data)
            if serializers.is_valid():
                return _success_data(status_code=202, data=serializers.data)
            return _error_data(status_code=400, message=serializers.error_messages, detail=serializers.errors)
           
           

    if request.method =='DELETE':
        zakas_id = request.data.get('zakas_id')
        if zakas_id is not None:
            data = ZakasProduct.objects.get(id=zakas_id)
            data.delete()
            return _success_data(status_code=204, data=f"dalete {zakas_id} success")
        return _error_data(status_code=404, message="zakas id not fount", detail=None)

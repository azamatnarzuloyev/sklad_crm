from rest_framework.decorators import api_view, APIView , permission_classes
from rest_framework.response import Response
from rest_framework import status
from permission.permissions import DokonUserAuthentication
from product.utilts import product_arxiv_funtions
from .serializers import ProductsSerialziersJson, AllShopSerialziers, ProductsShopSerialziersJson
from product.models import Product , ProductJsonArxiv
from magazin.models import AllShop
from django.utils.timezone import make_aware
import datetime
naive_datetime = datetime.datetime.now()
date_times = datetime.date
from django.conf import settings
settings.TIME_ZONE  # 'UTC'
aware_datetime = make_aware(naive_datetime)
import json
from django.db.models.query import   QuerySet
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from drf_spectacular.utils import extend_schema
# from product.scripts.product import runApp
from datetime import date
# from product.views import allProduct_import_funtion

from django.http import JsonResponse




@api_view(['DELETE'])
def delete_all(request):
    if request.method =="DELETE":
        return Response({"data": "delete"})




@extend_schema (
        request=ProductsShopSerialziersJson,
        responses= {
            200: ProductsShopSerialziersJson
        }
)
@api_view(['GET', 'POST'])
# @permission_classes([DokonUserAuthentication])
def product_shop(request):
    if request.method =="GET":
        user = request.user
        if str(user) == "AnonymousUser":
            shop_id = request.data['shop_id']
        else:
            all_shop = AllShop.objects.get(userId__id=user.id)
            shop_id = str(all_shop.id)
        try:
            product = Product.objects.get(material_nomer=request.data['material_nomer'])
            serializer = ProductsShopSerialziersJson(product)
            for i in serializer.data['dokon_tavarlar']:
                if i['id'] in shop_id:
                    if request.data['serena'] is not None:
                        if request.data['serena'] in i['array_serena']:
                            return  Response({"status": True, "serena": request.data['serena'] })
                        else:
                            return Response({"status": False,  "serena": request.data['serena'] })
                    return Response(i)
                break
            return Response(serializer.data)
        except Exception as e:
            return Response({"errors": f"{e}"})
        
    if request.method  == "POST":
        try:
            product_datSet = []
            user = request.user
            if str(user) == "AnonymousUser":
                data_set = request.data['shop_id']
            else:
                all_shop = AllShop.objects.get(userId__id=user.id)
                data_set = str(all_shop.id)
            products_one=  Product.objects.first()
            index = None
            for f in range(0, len(products_one.dokon_tavarlar)):
                 if  str(products_one.dokon_tavarlar[f]['id'])== str(data_set):
                      index = f 
                      break   
            products_list = Product.objects.all().order_by('id')
            # data_product = Product.objects.raw("SELECT id, material_nomer, price,  product_name, dokon_tavarlar FROM product_product ORDER BY id ASC")
            for product in products_list:
                data = {
                    "product_id": product.id,
                    "price": product.price,
                    "product_name": product.product_name,
                    "tavar_ckidka": product.tavar_ckidka,
                    "material_nomer": product.material_nomer,
                    "shop_data": product.dokon_tavarlar[index]  
                 }
                product_datSet.append(data)
            return JsonResponse(product_datSet, safe=False)  
        except Exception as e:
            return Response({"data":None,"errors":True,"message": f"{e}"})



  

def _test_product(i, shop_id):
        errors_serena = []
        if i['product_serena'] is not None:
            product = Product.objects.get(id=i['id'])
            for s in product.dokon_tavarlar:
                if s['id'] == str(shop_id):
                    for j in i['product_serena']:
                        if j in s['array_serena']:errors_serena.append(j)   
            if errors_serena:return ({"product_id": product.id, "errors": True,"masage": errors_serena,})
            else:return ({"errors": False,})
        else:
            product = Product.objects.get(id=i['id'])
            for s in product.dokon_tavarlar:
                if s['id'] == str(shop_id):
                    if((s['product_count']) > int(i['product_count'])):
                        s['product_count'] = s['product_count'] - i['product_count']  
                    else:
                        errors_serena.append(i['product_count'])
            if errors_serena:
                return ({
                        "product_id": product.id,
                        "errors": True,
                        "masage": errors_serena,
                    })
            else:
                return ({
                    "errors": False
                })
            



def _test_product_put(i, shop_id):
        errors_serena = []
        if i['product_serena'] is not None:
            product = Product.objects.get(id=i['id'])
            for s in product.dokon_tavarlar:
                if s['id'] == str(shop_id):
                    for j in i['product_serena']:
                        if j in s['array_serena']:
                            errors_serena.append(j)   
            if errors_serena:
                    return ({
                        "product_id": product.id,
                        "errors": True,
                        "masage": errors_serena,
                    })
            else:
                    return ({
                        "errors": False,

                    })
        else:
           
                return ({
                    "errors": False
                })

def _append_product(i, shop_id):
        if i['product_serena'] is not None:
            product = Product.objects.get(id=i['id'])
            for j in i['product_serena']:
                for s in product.dokon_tavarlar:
                    if s['id'] == str(shop_id):
                        s['array_serena'].append(j)
                        product.save()  
        else:
            product = Product.objects.get(id=i['id'])
            for s in product.dokon_tavarlar:
                if s['id'] == str(shop_id):
                        s['product_count'] = s['product_count'] + i['product_count']
                        product.save()
# ---------------------------------------------------------------------------------------
                        




class ProductPostGetUpdatedelete(APIView):
    @extend_schema(

        request=ProductsSerialziersJson,
  
        responses={
        
            202: "data get post update"
            },
       
        
        ) 
    def put(self, request, format=None):
        user = request.user
        if str(user) == "AnonymousUser":
            shop_id = request.data['shop_id']
        else:
            all_shop = AllShop.objects.get(userId__id=user.id)
            if not(all_shop.sklad):
                return Response({
                    "errors": "bu sklad emas siz tavarni update qilolmaysiz"
                })
            shop_id = str(all_shop.id)
        if request.data['product_count'] is not None or request.data['product_serena'] is not None:
            product_put = _test_product_put(i=request.data, shop_id=shop_id)
            if product_put['errors']:
                return Response(product_put)
            else:
                _append_product(i=request.data, shop_id= shop_id)
                
        produc = Product.objects.get(id = request.data['id'])
        serializer = ProductsSerialziersJson(produc, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors)

    


@extend_schema (
        request=ProductsShopSerialziersJson,
        responses= {
            202: ProductsShopSerialziersJson
        }
)
@api_view(['PUT'])
@permission_classes([DokonUserAuthentication])
def product_update_views(request, pk=None):
     if request.method =='PUT':
          product = Product.objects.get(id=pk)
          serialzier = ProductsSerialziersJson(product, data=request.data)
          if serialzier.is_valid():
               serialzier.save()
               return Response(serialzier.data)
          return Response(serialzier.errors, status=status.HTTP_202_ACCEPTED)
     

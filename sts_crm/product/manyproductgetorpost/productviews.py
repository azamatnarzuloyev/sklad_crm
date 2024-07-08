from rest_framework.response import Response
from rest_framework.request import Request
from permission.permissions import DokonUserSHopAuthentication
from product.models import Product , ProductNewsImport
from magazin.models import AllShop
from rest_framework.decorators import api_view , permission_classes
from rest_framework.views import APIView
from product.manyproductgetorpost.serialziers import ProductPostSerialzier, ProductPutSerialzier 
from drf_spectacular.utils import extend_schema 
from product.newData.serializers import  ProductsSerialziersJson, ProductsShopSerialziersJson
from datetime import   datetime
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from product.serenapath import serena_path
from django.utils import timezone
from datetime import date
# -------------------------------------------------------------------------------------



# -------------------------------------------------------------------------------------

def _import_data(data , status):
    import_data :bool = ProductNewsImport.objects.filter(createStatus_number=0).exists()
    import_data_one :bool = ProductNewsImport.objects.filter(createStatus_number=1).exists()
    if import_data and data:
        product =  ProductNewsImport.objects.filter(createStatus_number=0).first()
        product.products = []
        product.products.append(data)
        product.save()
    if status and ProductNewsImport.objects.filter(createStatus_number=0).exists():
        products =  ProductNewsImport.objects.filter(createStatus_number=0).first()
        products.createStatus_number = 1  
        products.save()
             
    if import_data_one and data:
        data_status = False
        product_data =  ProductNewsImport.objects.filter(createStatus_number=1).first()
        for j in product_data.products:
            if data['id'] == j['id']:
                data_status = True
                if j.get('product_serena') is not None:
                    j['product_serena'] = j['product_serena'] + data['product_serena']
                    product_data.save()
                else:
                    j['product_count'] = j['product_count'] + data['product_count']
                    product_data.save()
        if not(data_status):
            product_data.products.append(data)
            product_data.save()

#----------------------------------------------------------------------------
@extend_schema (
        request=ProductPutSerialzier,
        responses= {
            200: ProductPutSerialzier
        }
)
@api_view(['PUT'])
# @permission_classes([DokonUserSHopAuthentication])
def product_update_funtion(request:Request):
    if request.method =='PUT':
        try:
            dokon_sklad = AllShop.objects.get(sklad=True)
            products = request.data.get("products")
            products_one = Product.objects.first()
            index = None
            for f in range(0, len(products_one.dokon_tavarlar)):
                if  str(products_one.dokon_tavarlar[f]['id'])== str(dokon_sklad.pk):
                    index = f 
                    break 
        except Exception as e:
            return Response({"data":None, "errors":True, "message": ""})
        if products is not None:
            try:
                err_product = []
                serenaPath = []
                for product in products:
                    product_serena = product['product_serena']
                    prod = Product.objects.get(id=product['id'])
                    if prod.serenaTrue_countFalse and index is not None:
                        product_serena = list(set(product_serena))
                        arr_serena = [x for x in set(product["product_serena"]) if x in set(prod.dokon_tavarlar[index]["array_serena"])]
                        if len(arr_serena)>0:
                            arr_data = {
                                "product_id": product['id'],
                                "product_name": prod.product_name,
                                "product_serena": arr_serena
                            }
                            err_product.append(arr_data)
                if len(err_product)> 0:
                    return Response(err_product)
                for product in products:
                    product_id = product['id']
                    product_count = product.get('product_count')
                    product_serena =  product.get('product_serena')
                    prod = Product.objects.get(id=product_id)
                    if not(prod.serenaTrue_countFalse)  and index is not None:
                        product_count = int(product_count)
                        prod.dokon_tavarlar[index]['product_count'] =int(prod.dokon_tavarlar[index]['product_count']) + product_count
                        prod.save()
                    if prod.serenaTrue_countFalse and index is not None:
                        product_serena = list(set(product_serena))
                        prod.dokon_tavarlar[index]["array_serena"] = list(set(prod.dokon_tavarlar[index]["array_serena"]) | set(product["product_serena"]))
                        prod.save()
                        data = {
                            "product_id": prod.pk,
                            "product_name": prod.product_name,
                            "material_nomer": prod.material_nomer,
                            "serena": list(set(product['product_serena'])),
                            "path": {
                                "yuboruvchi": "xitoy",
                                "qabul_qiluvchi": dokon_sklad.dokon_name,
                                "tavar": True,
                                "savdo_status":False,
                                "putty_status": False,
                                "vazvrat_status": False,
                                "shartnoma": False,
                                "clinet_id": "",
                                "client_name": "",
                                "date": f"{date.today()}",
                                "date_time": f"{timezone.now().hour}:{timezone.now().minute}",
                            },
                        }
                        serenaPath.append(data)
                if len(serenaPath) >0:
                    serena_path(products=serenaPath)
                return Response({"data": "success", "errors":False, "message": ""})
            except Exception as e:
                return Response({"data": None, "errors":True, "message": f"{e}"})
        
        return Response({"data": None, "errors":True, "message": "products not fount"})

def _import_data_set(data , status):
    import_data :bool = ProductNewsImport.objects.filter(createStatus_number=0).exists()
    import_product :bool = ProductNewsImport.objects.filter(createStatus_number=1).exists()
    if import_data and data:
        product =  ProductNewsImport.objects.filter(createStatus_number=0).first()
        product.products = []
        product.products.append(data)
        product.save()
    if status and ProductNewsImport.objects.filter(createStatus_number=0).exists():
        products =  ProductNewsImport.objects.filter(createStatus_number=0).first()
        products.createStatus_number = 1  
        products.save()
    if import_product:
        product =  ProductNewsImport.objects.filter(createStatus_number=1).first()
        product.products.append(data)
        product.save()


class ProductPostnews(APIView):
    # permission_classes = [DokonUserSHopAuthentication]

    @extend_schema(
        request=ProductsSerialziersJson,
        responses={
            200: ProductsShopSerialziersJson,
            # 201: ProductsSerialziersJson,
            # 202: ProductsSerialziersJson
            },
            description="data get post update"
        ) 
    def get(self, request, pk=None,  format=None):
        if pk is not None:
            product = Product.objects.get(id=pk)
            serializer = ProductsShopSerialziersJson(product)
            return Response(serializer.data)
        paginator = PageNumberPagination()
        paginator.page_size = 20
        product = Product.objects.all().order_by("id")
        query = request.GET.get("q", "")
        queryset = Product.objects.filter(
                    Q(product_name__icontains=query),
                ).all()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProductsShopSerialziersJson(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        request=ProductsSerialziersJson,
        responses={
            # 200: ProductsShopSerialziersJson,
            201: ProductsSerialziersJson,
            # 202: ProductsSerialziersJson
            },
            description="data get post update"
        ) 
    def post(self, request, format=None):
        prod_serialzier = ProductPostSerialzier(data=request.data)
        if prod_serialzier.is_valid():
            try:
                serenaPath = []
                serenaTrue_countFalse = prod_serialzier.data.get('serenaTrue_countFalse')
                product_serena = request.data.get('product_serena', None)
                product_count = request.data.get('product_count', None)
                product_name = prod_serialzier.data.get('product_name')
                sklad = AllShop.objects.get(sklad=True)
                dokon_product = AllShop.objects.filter(sklad=False, vendor=False)
                dokon_tavarlar = []
                if serenaTrue_countFalse:
                    dokon_count = None
                    sklad_count = None
                    skladSerena = list(set(product_serena))
                    dokon_serena = []
                else:

                    skladSerena  = None
                    sklad_count = int(product_count)
                    dokon_serena = None
                    dokon_count = 0

                sklad_product = {
                        "id": str(sklad.pk),
                        "store_name": sklad.dokon_name,
                        "sklad": True,
                        "product_count": sklad_count,
                        "vendor": False,
                        "birja": False,
                        "array_serena": skladSerena
                    
                    }
                dokon_tavarlar.append(sklad_product)
                for dokon in dokon_product:
                    productAppendDokon = {
                        "id": str(dokon.pk),
                        "store_name": dokon.dokon_name,
                        "sklad": True,
                        "product_count": dokon_count,
                        "vendor": False,
                        "birja": False,
                        "array_serena": dokon_serena
                    }
                    dokon_tavarlar.append(productAppendDokon)
                request.data['dokon_tavarlar'] = dokon_tavarlar
                    
                serialzers = ProductsSerialziersJson(data=request.data)
                if serialzers.is_valid():
                    serialzers.save()
                    id = serialzers.data.get('id')
                    product_name = serialzers.data.get('product_name')
                    material_nomer = serialzers.data.get('material_nomer')
                    data = {
                        "id": id,
                        "product_name": product_name,
                        "product_serena": product_serena,
                        "product_count": product_count,
                        "time": f"{datetime.now()}"
                        }
                    data_import = _import_data_set(data=data, status=True)
                    if serenaTrue_countFalse:
                        data = {
                                "product_id": id,
                                "product_name": product_name,
                                "material_nomer": material_nomer,
                                "serena": skladSerena,
                                "path": {
                                    "yuboruvchi": "xitoy",
                                    "qabul_qiluvchi": sklad.dokon_name,
                                    "tavar": True,
                                    "savdo_status":False,
                                    "putty_status": False,
                                    "vazvrat_status": False,
                                    "shartnoma": False,
                                    "clinet_id": "",
                                    "client_name": "",
                                    "date": f"{date.today()}",
                                    "date_time": f"{timezone.now().hour}:{timezone.now().minute}",
                                },
                            }
                        serenaPath.append(data)
                    if len(serenaPath)>0:
                        serena_path(products=serenaPath)
                           
                    return Response(
                    {
                        "data": {
                            "product": serialzers.data,
                            "importData": data_import
                        },
                        "errors": False,
                        "status": 200,
                        "status_code": 201,
                        "message": "",
                        "detail": "",
                        "token": "",
                    }
                    )
            except Exception as e:
                 return Response({"data": None, "errors":True, "message":f"{e}"})
            return Response({"data":None, "errora":True,"message":serialzers.errors})

        return Response( {"data":None,"errors":True, "message":prod_serialzier.errors})



new_productpost_funtion = ProductPostnews.as_view()





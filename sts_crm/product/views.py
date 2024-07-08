from rest_framework.response import Response 
from product.newData.serializers import ProductsShopSerialziersJson
from .serializers import  ProductSerializer, ProductjsonFiledSerialzier , NewImportProductSerialzier
from .models import Product , ProductJsonArxiv  , ProductNewsImport
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from asyncio.log import logger
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from datetime import date
import json
import re

@extend_schema (
        request=ProductsShopSerialziersJson,
        responses= {
            200: ProductsShopSerialziersJson
        }
)
@api_view(['GET'])
def product_detail(request, pk):
    """
    Product detail request pk
    """
    if request.method =="GET":
        try:
            product = Product.objects.get(id=pk)
            serieliser = ProductsShopSerialziersJson(product)
            return Response(serieliser.data)
        except Product.DoesNotExist:
            return Response({"product":"not fount"})





@api_view(['GET','POST','PUT'])
def product_views(request):
    """
    product ko'rish yangi tavar qo'shish bitta tavarni ko'rish 
    """
    paginator = PageNumberPagination()
    paginator.page_size = 10
    if request.method =="GET":

        try:   
            
            product = Product.objects.all()
            result_page = paginator.paginate_queryset(product, request)
            serializer = ProductSerializer(result_page , many=True)
            return paginator.get_paginated_response(serializer.data)
        except:
            return Http404({"page not fount"})  
              
  

@api_view(['GET', 'POST'])
def product_json_arxiv(request):
    """ Barcha tavarlarni kunlik arxivlash """
    if request.method =="POST":
        product = Product.objects.all()
        serializer = ProductjsonFiledSerialzier(product, many=True)
        data = json.dumps(serializer.data)
        json_data = json.loads(data)
        if ProductJsonArxiv.objects.filter(date=date.today()).exists():
            return Response({"data": "update"})
        product_json = ProductJsonArxiv.objects.create(
            date = date.today(),

            json_product = json_data
        )
        product_json.save()

        return Response({
            "data" :"successes"
        })
    if request.method =='GET':
        news_data = []
        try:
            product_data = request.data['product_data']
            date_product = request.data['date']
        except:
            return Response({
                "date": "errors product_data and date"
            })
        product_json = ProductJsonArxiv.objects.get(date=date_product)
        news = product_data.lower()
        for i in product_json.json_product:
            indexs = i['product_name'].lower()
            result =  re.findall(news ,indexs)
            if result:
                news_data.append(i)
        return Response ({
            "date": product_json.date, 
            "len": len(news_data),
            "product": news_data,

        })
    
@api_view(['POST'])
def import_product(request):
    if request.method =="POST":
        """ 
        import data get or create agar yopishni true qilib yuborilsa yopib yangi bir import data ochamiz 
         agar ynagi import data ochishi uchun import_id yuporiladi     
        """
        yaratish = False
        import_bool: bool = ProductNewsImport.objects.filter(createStatus_number=1).first()
        counts = ProductNewsImport.objects.count()
        yopish = request.data.get('yopish')
        if yopish and import_bool:
            data_set = ProductNewsImport.objects.filter(createStatus_number=1).first()
            data_set.createStatus_number = 2
            data_set.close_data = date.today()
            data_set.save()
            yaratish = True

        data_import: bool = ProductNewsImport.objects.filter(createStatus_number=0).exists()
        if data_import:
            importData = ProductNewsImport.objects.filter(createStatus_number=0).first()
            return Response ({
                "data": None,
                "errors": True,
                "message": f"import_id= {importData.import_id} malumotlari ochilgan ochishdan oldin birinchi yopishingiz kerak yopish uchun yopish = true yuboring  ",
                "detail": "",
                "token": "",
            })
        if yaratish or bool(int(counts)  < 1):
            if request.data.get('import_id') is None:
                return Response({
                     "data": None,
                        "errors": True,
                        "message": "import id required",
                        "detail": None,
                        "token": ""
                })
            
            import_serialzier = NewImportProductSerialzier(data=request.data)
            if import_serialzier.is_valid():
                import_serialzier.save()
                return Response(
                    {
                        "data": import_serialzier.data,
                        "errors": False,
                        "message": "",
                        "detail": "",
                        "token": ""

                    }
                )
           
            return Response({
                         "data": None,
                        "errors": True,
                        "message": import_serialzier.error_messages,
                        "detail": import_serialzier.errors,
                        "token": ""
                })
        else:
            return Response ({
                        "data": None,
                        "errors": False,
                        "message": "Kiritilgan malumot to'gri kelmadi ",
                        "detail": "",
                        "token": ""
            })

    


@api_view(['GET'])
def import_data_get(request):
    if request.method =='GET':
        """ Import malumotlari ochilgan yoki ochilmagni tekshirish """
        import_data :bool = ProductNewsImport.objects.filter(createStatus_number=1).exists()
        import_data_null :bool = ProductNewsImport.objects.filter(createStatus_number=0).exists()
        product_data = ProductNewsImport.objects.filter(createStatus_number=1).first()
        import_serialzier = NewImportProductSerialzier(product_data)
        if import_data:
            return Response (
                {
                    "data": {
                        "message": "Import data malumotlari ochilgan",
                        "import_data": import_serialzier.data
                    },
                    "status": 200,
                    "error" : False,
                    "massage": "",
                    "token": "" 
                }
            )
        
        if import_data_null:
            data_set = ProductNewsImport.objects.filter(createStatus_number=0).first()
            return Response(
                {
                    "data": "",
                    "status": 200,
                    "error" : True,
                    "import_id": data_set.import_id,

                    "massage": f" Import_id = {data_set.import_id} ochilgan ",
                    "token": "" 
                }
            )


        else:
            return Response(
                {
                    "data": "",
                    "status": 200,
                    "error" : True,
                    "import_id": None,
                    "massage": "Yangi Import_id ochishingiz kerak",
                    "token": "" 
                }
            )

    


           
                

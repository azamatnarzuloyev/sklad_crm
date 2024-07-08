from rest_framework.response import Response
from rest_framework import status
from magazin.models import DaySellerShop , AllShop 
from product.models import Product
from rest_framework.decorators import api_view , permission_classes
from rest_framework.views import APIView
from django.db.models import Q
from permission.permissions import DokonUserAuthentication
from datetime import date
from savdo.serializers import DaySellerShopSerialziers, DaySellerShopSerialziersMobile
from django.shortcuts import get_object_or_404 
from django.http import JsonResponse
from datetime import date

@api_view(['GET'])
@permission_classes([DokonUserAuthentication])
def mobile_product_list(request):
    """
    key  headers 
    search: string,
    all_product: bool
    """
    if request.method =='GET':
        user = request.user
        shop_bool:bool = AllShop.objects.filter(userId__id=user.id)
        search = request.GET.get('search')
        all_product = request.GET.get('all_product', False)
        
        if search is not None:
            product = Product.objects.filter(
                    Q(product_name__icontains=search)
                )[:20]
        else:
            product = Product.objects.raw("SELECT id, material_nomer, price,  product_name, dokon_tavarlar FROM product_product ORDER BY id ASC")

        products  = []
        counts = len(product)
        if shop_bool:
            dokon = AllShop.objects.get(userId__id=user.id)
            dokon_id = dokon.id
            for i in product:
                for j in i.dokon_tavarlar:
                    if str(j['id']) == str(dokon_id):
                        data = {
                                "product_id": i.id,
                                "price": i.price,
                                "product_name": i.product_name,
                                "tavar_ckidka": i.tavar_ckidka,
                                "material_nomer": i.material_nomer,
                                "dokon_tavarlar": j
                        }
                        products.append(data)
                        break
           
            return Response(
            {   "count": counts,
                "data": products,
                "errors": False,
                "message": "",
                "detail": "",
                "token": ""
            }
            )
        if not(shop_bool) or all_product:
            for i in product:
                data = {
                    "product_id": i.id,
                    "price": i.price,
                    "product_name": i.product_name,
                    "tavar_ckidka": i.tavar_ckidka,
                    "material_nomer": i.material_nomer,
                    "dokon_tavarlar": i.dokon_tavarlar
                    }
                products.append(data)
          
            return Response({
                "count": counts,
                "data": products,
                "errors": False,
                "message": "",
                "detail": "",
                "token": ""
            })
        

def __savdo_statistika(request, all_savdo):
    user = request.user 
    all_shop = AllShop.objects.get(userId__id=user.id)
    if all_shop.sklad:
        if all_savdo:
           daySavdo = DaySellerShop.objects.all()
        else:
            daySavdo = DaySellerShop.objects.filter(sellerdate_create=date.today(),)

    else:
        if all_savdo:
            daySavdo = DaySellerShop.objects.filter(user_id=user.id)
        else:
            daySavdo = DaySellerShop.objects.filter(sellerdate_create=date.today(), user_id=user.id)

    umumiy_sum =  0
    cashbacktushganSum = 0
    cashbackTolov = 0
    qarz = 0
    naxt = 0
    kartadantolow =0
    firmadantolov = 0
    depozittolov = 0
   


    return {
        "umumiy_sum": umumiy_sum,
        "cashbackTolov": cashbackTolov,
        "qarz": qarz,
        "naxt": naxt,
        "kartadantolow": kartadantolow,
        "firmadantolov": firmadantolov,
        "depozittolov": depozittolov

    }
            
@api_view(['GET'])
# @permission_classes([DokonUserAuthentication])
def dokon_savdo_funtion(request):
    """ 
    date: date,
    all_shop: bool
    """
    if request.method =='GET':
        
        
        if request.GET.get('new') is not None:
            data = DaySellerShop.objects.all()
            serialziers=  DaySellerShopSerialziersMobile(data , many=True)
            return JsonResponse({
                "data": serialziers.data
            }, safe=False)
        user = request.user

        date_filter = request.GET.get('date', date.today())
        all_savdo = request.GET.get('all_savdo', False)
        shop_bool:bool = AllShop.objects.filter(userId__id=user.id).exists()
        if shop_bool:
            statistika = __savdo_statistika(request, all_savdo=all_savdo)
            dokon_bool = AllShop.objects.get(userId__id=user.id)
            if dokon_bool.sklad:

                if all_savdo:
                    day_savdo = DaySellerShop.objects.all().order_by('-sellerdate_create')
                    dayShop_serialzier = DaySellerShopSerialziersMobile(day_savdo, many=True)
                else:
                    day_savdo = DaySellerShop.objects.filter(sellerdate_create=date_filter)
                    dayShop_serialzier = DaySellerShopSerialziersMobile(day_savdo, many=True)
            else:
                if all_savdo:
                    day_savdo = DaySellerShop.objects.filter(user_id=user.id).order_by('-sellerdate_create')
                    dayShop_serialzier = DaySellerShopSerialziersMobile(day_savdo, many=True)
                else:
                    day_savdo = DaySellerShop.objects.filter(sellerdate_create=date_filter, user_id=user.id).order_by('-sellerdate_create')
                    dayShop_serialzier = DaySellerShopSerialziersMobile(day_savdo, many=True)

            return Response(
                {
                    "data":  {"statistika": statistika, "savdolar":dayShop_serialzier.data},
                    "errors": False,
                    "message": "",
                    "detail": "",
                }
            )

        else:
            if all_savdo:
                day_savdo = DaySellerShop.objects.all().order_by('-sellerdate_create')
                dayShop_serialzier = DaySellerShopSerialziersMobile(day_savdo, many=True)
            else:
                day_savdo = DaySellerShop.objects.filter(sellerdate_create=date_filter).order_by('-sellerdate_create')
                dayShop_serialzier = DaySellerShopSerialziersMobile(day_savdo, many=True)
            return Response(
                {
                    "data": dayShop_serialzier.data,
                    "errors": False,
                    "message": "",
                    "detail": "",
                }
            )


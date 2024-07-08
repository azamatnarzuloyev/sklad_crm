from rest_framework.views import APIView
from rest_framework import status
from .models import Product
from magazin.models import AllShop, DaySellerShop
from django.http import JsonResponse
from rest_framework.response import Response
from django.db.models import Q


import datetime


def next_week():
    today = datetime.date.today()
    return [today + datetime.timedelta(days=1), today + datetime.timedelta(days=7)]


class ProductSavdoViews(APIView):
    def get(self, request, pk=None, format=None):
        """one product order filter"""
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        one_day = request.GET.get("one_day")
        products = []
        savdo_status = ""
        product_bool: bool = Product.objects.filter(id=pk).exists()
        if not (product_bool):
            return Response(
                {
                    "data": None,
                    "errors": True,
                    "status": 200,
                    "status_code": 404,
                    "message": "Product id  not fount",
                    "detail": "",
                    "token": "",
                }
            )
        if start_date is not None and end_date is not None:
            savdo = DaySellerShop.objects.filter(
                Q(sellerdate_create__gte=start_date, sellerdate_create__lte=end_date)
            )
            savdo_status = f"{start_date}  {end_date} gacha savdolar"
        elif one_day is not None:
            savdo_status = f"{one_day} kun uchun savdolar "
            savdo = DaySellerShop.objects.filter(
                Q(sellerdate_create__range=next_week())
            )

        else:
            savdo_status = "barcha savdolar"
            savdo = DaySellerShop.objects.filter(sellerdate_create=one_day)

        if savdo.count() > 0:
            pass
        else:
            # Product.objects.raw(" SELECT id, material_nomer, price,  product_name, dokon_tavarlar FROM product_product ORDER BY id ASC")
            day_savdo = DaySellerShop.objects.all()
            for i in day_savdo:
                for j in i.product_arr:
                    if j["id"] == pk:
                        shop_name = AllShop.objects.get(userId=i.user_id)
                        j["shop_name"] = shop_name.dokon_name
                        products.append(j)
        if products:
            return Response(
                {
                    "data": products,
                    "savdo_status": savdo_status,
                    "errors": False,
                    "status": 200,
                    "status_code": 200,
                    "message": "",
                    "detail": "",
                    "token": "",
                }
            )

        return JsonResponse(
            {
                "data": [],
                "errors": False,
                "status": 200,
                "status_code": 200,
                "message": "",
                "detail": "",
                "token": "",
            }
        )

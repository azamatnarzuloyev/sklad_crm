from rest_framework import serializers
from django.http import JsonResponse
from magazin.models import DaySellerShop, Savdo, AllShop
from product.models import Product
from rest_framework.request import Request
from utills.productupdate import ProductUpdate, VendorProductsUpdate
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from datetime import date


class SavdoDeleteViews(APIView):
    def delete(self, pk, request):
        checkSavdo = get_object_or_404(pk, DaySellerShop)
        arxiv = False
        if checkSavdo:
            day_savdo = DaySellerShop.objects.get(id=pk, sellerdate_create=date.today())
            shop = AllShop.objects.get(userId=day_savdo.user_id)
            products = day_savdo.product_arr
            if shop.vendor:
                VendorProductsUpdate(products=products, shop_id=shop.pk).product__append
            else:
                ProductUpdate(products=products, shop_id=shop.pk).append_product
            if arxiv:
                pass
            day_savdo.delete()
            return JsonResponse(
                {"data": "delete success", "errors": False, "message": ""}, safe=False
            )
        return JsonResponse(
            {
                "data": None,
                "errors": True,
                "messsage": "Savdoni o'chirib bo'lmaydi savdo yaralganiga bir kundan kam bo'lishi kerak",
            },
            safe=False,
        )

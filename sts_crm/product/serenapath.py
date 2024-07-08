from .models import (
    ProductSerenapathOne,
    ProductSerenapathTwo,
    ProductSerenapathFour,
    ProductSerenapathEnd,
    ZerenaPathStatus,
)
from datetime import date
from django.http import JsonResponse
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.views import APIView


def _tekshirish_fn():
    """yil boyicha tekshirish yillar boyicha case [1..4] bazaga joylashni tekshirish"""
    date_data = date.today().year
    test_bool: bool = ZerenaPathStatus.objects.filter(datatest="test").exists()
    if not (test_bool):
        statusserena = ZerenaPathStatus()
        statusserena.year_filter = date_data
        statusserena.save()
        return statusserena.count_status
    if test_bool:
        zerana_path = ZerenaPathStatus.objects.get(datatest="test")
        zerana_path.count_status
        match zerana_path.count_status:
            case 1:
                if zerana_path.year_filter == date_data:
                    return zerana_path.count_status
                else:
                    if zerana_path.delete_bool:
                        prod_ser = ProductSerenapathTwo.objects.all()
                        prod_ser.delete()
                    zerana_path.count_status = 2
                    zerana_path.save()
                    return zerana_path.count_status
            case 2:
                if zerana_path.year_filter == date_data:
                    return zerana_path.count_status
                else:
                    if zerana_path.delete_bool:
                        prod_serr = ProductSerenapathFour.objects.all()
                        prod_serr.delete()
                    zerana_path.count_status = 3
                    zerana_path.save()
                    return zerana_path.count_status
            case 3:
                if zerana_path.year_filter == date_data:
                    return zerana_path.count_status
                else:
                    if zerana_path.delete_bool:
                        prod_seren = ProductSerenapathEnd.objects.all()
                        prod_seren.delete()
                    zerana_path.count_status = 4
                    zerana_path.save()
                    return zerana_path.count_status
            case 4:
                if zerana_path.year_filter == date_data:
                    return zerana_path.count_status
                else:
                    prod_serena = ProductSerenapathOne.objects.all()
                    prod_serena.delete()
                    zerana_path.count_status = 1
                    zerana_path.delete_bool = True
                    zerana_path.save()
                    return zerana_path.count_status


def _stetment_prod(tekshirish, data):
    match tekshirish:
        case 1:
            prod_list = (
                ProductSerenapathOne.objects.filter(
                    product_id=data["product_id"]
                ).exists()
                and ProductSerenapathOne.objects.get(product_id=data["product_id"])
                or None
            )
            if prod_list is not None:
                for serena in data["serena"]:
                    if prod_list.serena_path.get(serena) is not None:
                        prod_list.serena_path[serena].append(data["path"])
                        prod_list.save()
                    else:
                        prod_list.serena_path[serena] = [data["path"]]
                        prod_list.save()
            else:
                prod_list = ProductSerenapathOne()
                prod_list.product_id = data["product_id"]
                prod_list.product_name = data["product_name"]
                prod_list.material_nomer = data["material_nomer"]
                prod_list.serena_path = {}
                for serena in data["serena"]:
                    prod_list.serena_path[serena] = [data["path"]]
                    prod_list.save()

            return {
                "product_name": prod_list.product_name,
                "product_id": prod_list.product_id,
                "material_nomer": prod_list.material_nomer,
                "serena_path": prod_list.serena_path,
            }

        case 2:
            prod_list = (
                ProductSerenapathTwo.objects.filter(
                    product_id=data["product_id"]
                ).exists()
                and ProductSerenapathTwo.objects.get(product_id=data["product_id"])
                or None
            )
            if prod_list is not None:
                for serena in data["serena"]:
                    if prod_list.serena_path.get(serena) is not None:
                        prod_list.serena_path[serena].append(data["path"])
                        prod_list.save()
                    else:
                        prod_list.serena_path[serena] = [data["path"]]
                        prod_list.save()
            else:
                prod_list = ProductSerenapathTwo()
                prod_list.product_id = data["product_id"]
                prod_list.product_name = data["product_name"]
                prod_list.material_nomer = data["material_nomer"]
                prod_list.serena_path = {}
                for serena in data["serena"]:
                    prod_list.serena_path[serena] = [data["path"]]
                    prod_list.save()
            return None
        case 3:
            prod_list = (
                ProductSerenapathFour.objects.filter(
                    product_id=data["product_id"]
                ).exists()
                and ProductSerenapathFour.objects.get(product_id=data["product_id"])
                or None
            )
            if prod_list is not None:
                for serena in data["serena"]:
                    if prod_list.serena_path.get(serena) is not None:
                        prod_list.serena_path[serena].append(data["path"])
                        prod_list.save()
                    else:
                        prod_list.serena_path[serena] = [data["path"]]
                        prod_list.save()
            else:
                prod_list = ProductSerenapathFour()
                prod_list.product_id = data["product_id"]
                prod_list.product_name = data["product_name"]
                prod_list.material_nomer = data["material_nomer"]
                prod_list.serena_path = {}
                for serena in data["serena"]:
                    prod_list.serena_path[serena] = [data["path"]]
                    prod_list.save()
        case 4:
            prod_list = (
                ProductSerenapathEnd.objects.filter(
                    product_id=data["product_id"]
                ).exists()
                and ProductSerenapathEnd.objects.get(product_id=data["product_id"])
                or None
            )
            if prod_list is not None:
                for serena in data["serena"]:
                    if prod_list.serena_path.get(serena) is not None:
                        prod_list.serena_path[serena].append(data["path"])
                        prod_list.save()
                    else:
                        prod_list.serena_path[serena] = [data["path"]]
                        prod_list.save()
            else:
                prod_list = ProductSerenapathEnd()
                prod_list.product_id = data["product_id"]
                prod_list.product_name = data["product_name"]
                prod_list.material_nomer = data["material_nomer"]
                prod_list.serena_path = {}
                for serena in data["serena"]:
                    prod_list.serena_path[serena] = [data["path"]]
                    prod_list.save()


def serena_path(products):
    tekshirish = _tekshirish_fn()
    # data = {
    #     "product_id": 251,
    #     "product_name": "kamera",
    #     "material_nomer": "sdsds232",
    #     "serena": ["ww167202", "uf135393", "UP160491"],
    #     "path": {
    #         "data_id": "",
    #         "sender": "",
    #         "recipient": "",
    #         "status": "",
    #         "clinet_id": "",
    #         "client_name": "",
    #         "date": f"{date.today()}",
    #         "date_time": f"{timezone.now().hour}:{timezone.now().minute}",
    #     },
    # }
    for i in products:
        _stetment_prod(tekshirish, i)




class SerenaPathViews(APIView):
    def get(self, request):
        status_bool:bool =  ZerenaPathStatus.objects.count()
        if status_bool > 0:
            status_path = ZerenaPathStatus.objects.first().count_status
        else:
            status_path = ZerenaPathStatus.objects.create(year_filter=date.today().year)
            status_path.save()
            status_path = ZerenaPathStatus.objects.first().count_status

        match status_path:
            case 1:
                serenaOne = list(ProductSerenapathOne.objects.all().filter().values().order_by("?"))
                return Response(serenaOne)
            case 2:
                serenatwo = ProductSerenapathTwo.objects.all()
            case 3:
                serenaFour = ProductSerenapathFour.objects.all()
            case 4:
               serenaENd = ProductSerenapathEnd.objects.all()



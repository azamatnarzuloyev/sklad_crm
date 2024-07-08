from magazin.models import DaySellerShop, AllShop, Savdo, Klient
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User

from permission.permissions import DokonUserAuthentication
from puttyMagazin.models import DokonPutty
from .productschange import ProductDataUpdateAll, VendorProductUpdate
from django.http import JsonResponse
from datetime import date
from product.models import Product
from savdo.serializers import DaySellerShopSerialziers, SavdoSerializer
from savdo.tasks import serena_products, task_cashback_tushurish, task_depozit_tushirish
from product.serenapath import serena_path
from django.utils import timezone


class TolovUsullar:
    def __init__(self, hisobot, tolov_usullar, product_arr, shop_id):
        self.hisobot = hisobot
        self.shop_id = shop_id
        self.tolov_usullar = tolov_usullar
        self.product_arr = product_arr

    @property
    def hisobot_valadate(self):
        try:
            return dict(
                {
                    "tavar_summasi": float(self.hisobot["tavar_summasi"]),
                    "jami_skidka": float(self.hisobot["jami_skidka"]),
                    "olingan_summa": float(self.hisobot["olingan_summa"]),
                    "mahsulotUchun_tolov": float(self.hisobot["mahsulotUchun_tolov"]),
                    "tushgan_cashback_summa": (self.hisobot["tushgan_cashback_summa"])
                    is not None
                    and float(self.hisobot["tushgan_cashback_summa"])
                    or None,
                    "yechilgan_cashback_summa": (
                        self.hisobot["yechilgan_cashback_summa"]
                    )
                    is not None
                    and float(self.hisobot["yechilgan_cashback_summa"])
                    or None,
                    "depozitga_tushgan_summa": (self.hisobot["depozitga_tushgan_summa"])
                    is not None
                    and float(self.hisobot["depozitga_tushgan_summa"])
                    or None,
                }
            )
        except Exception as e:
            return {"errors": True, "message": f"{e}"}

    @property
    def hisobot_funion(self):
        pass

    @property
    def tolovUsullar_validate(self):
        try:
            return dict(
                {
                    "naxt": {
                        "active": bool(self.tolov_usullar["naxt"]["active"]),
                        "summa": float(self.tolov_usullar["naxt"]["summa"]),
                        "check": bool(self.tolov_usullar["naxt"]["check"]),
                    },
                    "plastik": {
                        "active": bool(self.tolov_usullar["plastik"]["active"]),
                        "summa": float(self.tolov_usullar["plastik"]["summa"]),
                        "check": bool(self.tolov_usullar["plastik"]["check"]),
                    },
                    "joyidaTolov": {
                        "active": bool(self.tolov_usullar["joyidaTolov"]["summa"]),
                        "summa": float(self.tolov_usullar["joyidaTolov"]["summa"]),
                        "check": bool(self.tolov_usullar["joyidaTolov"]["check"]),
                        "id_raqam": self.tolov_usullar["joyidaTolov"]["id_raqam"]
                        and int(self.tolov_usullar["joyidaTolov"]["id_raqam"]),
                    },
                    "qarz": {
                        "active": bool(self.tolov_usullar["qarz"]["active"]),
                        "summa": float(self.tolov_usullar["qarz"]["summa"]),
                        "update_at": self.tolov_usullar["qarz"]["update_at"],
                        "eslatma": {
                            "date": self.tolov_usullar["qarz"]["eslatma"]["date"],
                            "status": bool(
                                self.tolov_usullar["qarz"]["eslatma"]["status"]
                            ),
                        },
                    },
                    "depozit": {
                        "active": bool(self.tolov_usullar["depozit"]["active"]),
                        "summa": float(self.tolov_usullar["depozit"]["summa"]),
                        "check": bool(self.tolov_usullar["depozit"]["check"]),
                    },
                    "shartnoma": {
                        "active": bool(self.tolov_usullar["shartnoma"]["active"]),
                        "summa": float(self.tolov_usullar["shartnoma"]["summa"]),
                        "check": bool(self.tolov_usullar["shartnoma"]["check"]),
                        "id_raqam": self.tolov_usullar["shartnoma"]["id_raqam"]
                        and int(self.tolov_usullar["shartnoma"]["id_raqam"])
                        or None,
                    },
                }
            )
        except Exception as e:
            return dict({"errors": True, "message": f"{e}"})

    @property
    def tolov_funtion(self):
        if self.tolov_usullar["naxt"]["active"]:
            pass
        if self.tolov_usullar["plastik"]["active"]:
            pass
        if self.tolov_usullar["joyidaTolov"]["active"]:
            pass
        if self.tolov_usullar["qarz"]["active"]:
            pass
        if self.tolov_usullar["depozit"]["active"]:
            pass
        if self.tolov_usullar["shartnoma"]["active"]:
            pass

    @property
    def product_test(self):
        try:
            data = []
            for i in self.product_arr:
                arr = {
                    "product_id": int(i["product_id"]),
                    "product_name": str(i["product_name"]),
                    "product_serena": i["product_serena"] and list(i["product_serena"]),
                    "product_count": i["product_count"] and int(i["product_count"]),
                    "material_nomer": i["material_nomer"] and int(i["material_nomer"]),
                    "price": float(i["price"]),
                    # "discount_price": i['discount_price'] and float(i['discount_price']),
                    "tavar_ckidka": i["tavar_ckidka"] and float(i["tavar_ckidka"]),
                    "skidka_foiz": i["skidka_foiz"] and float(i["skidka_foiz"]),
                    # "cashback_bool": i['cashback_bool'] and bool(i['cashback_bool']),
                }
                data.append(arr)
            return {"data": data, "errors": False, "message": ""}
        except Exception as e:
            return {"data": data, "errors": True, "message": f"{e}"}


def tolov_usulini_aniqlash(tolov_usullar):
    status = None




class SavdoCreateViews(APIView):
    permission_classes = [DokonUserAuthentication]

    def post(self, request, format=None):
        try:
            product_arr = request.data.get("product_arr")
            hisobot = request.data.get("hisobot")
            tolov_usullar = request.data.get("tolov_usullar")
            client_uuid = request.data.get("client_uuid")
            user = request.user
            dokon = AllShop.objects.get(userId__id=user.id)
            shop_id = dokon.pk
            tolowlar = TolovUsullar(
                hisobot=hisobot,
                shop_id=shop_id,
                tolov_usullar=tolov_usullar,
                product_arr=product_arr,
            )
            hisobot_val, tolovUsul_val = (
                tolowlar.hisobot_valadate,
                tolowlar.tolovUsullar_validate,
            )

            if hisobot_val.get("errors", False):
                return JsonResponse(
                    {"data": None, "errors": True, "message": hisobot_val}, safe=False
                )
            if tolovUsul_val.get("errors", False):
                return JsonResponse(
                    {"data": None, "errors": True, "message": tolovUsul_val}, safe=False
                )
            prod = tolowlar.product_test
            if prod["errors"]:
                return JsonResponse(prod, safe=False)
            # -----------------------------------------------------------------

            vendor: bool = dokon.vendor
            if vendor:
                putty_bool: bool = DokonPutty.objects.filter(
                    dokon_uuid__id=dokon.id
                ).exists()
                if not (putty_bool):
                    putty_create = DokonPutty.objects.create(dokon_uuid=dokon)
                    putty_create.save()
                vendor_product = VendorProductUpdate(
                    products=product_arr, shop_id=shop_id
                ).product_test_remove
                if len(vendor_product) > 0:
                    return JsonResponse(
                        {"data": None, "errors": True, "message": vendor_product},
                        safe=False,
                    )

            if not (vendor):
                dokon_product: list = ProductDataUpdateAll(
                    products=product_arr, shop_id=shop_id
                ).test_product_remove
                if len(dokon_product) > 0:
                    return JsonResponse(
                        {"data": None, "errors": True, "message": dokon_product},
                        safe=False,
                    )
           
            savdo = (
                Savdo.objects.filter(
                    daySalesDate_create=date.today(), dokon_id__id=shop_id
                ).exists()
                and Savdo.objects.get(
                    daySalesDate_create=date.today(), dokon_id__id=shop_id
                )
                or None
            )
            if savdo is None:
                savdo = Savdo.objects.create(
                    dokon_id=dokon, savdo_status=True, daySalesDate_create=date.today()
                )
                savdo.save()
            if client_uuid is not None:
                client = Klient.objects.get(id=client_uuid)

            daySavdoCount = DaySellerShop.objects.count()
            daySavdo = DaySellerShop()
            daySavdo.daySavdo_nomer = int(daySavdoCount + 1000)
            daySavdo.year_filter = date.today().year
            daySavdo.savdo_uuid = savdo.pk
            daySavdo.sellerdate_create = date.today()
            daySavdo.user_id = dokon.userId.pk
            daySavdo.client_uuid = client
            daySavdo.product_arr = prod["data"]
            daySavdo.savdo_detail = {
                "hisobot": hisobot_val,
                "tolov_usullar": tolovUsul_val,
            }
            daySavdo.save()
            savdo.createdateseller.add(daySavdo)
            savdo.save()
            if vendor:
                VendorProductUpdate(
                    products=product_arr, shop_id=shop_id
                ).remove_product
            if not (vendor):
                ProductDataUpdateAll(
                    products=product_arr, shop_id=shop_id
                ).remove_product

            serialziers = DaySellerShopSerialziers(daySavdo, many=False)
            if daySavdo.client_uuid is not None and bool(
                daySavdo.savdo_detail["tolov_usullar"]["naxt"]["active"]
                or daySavdo.savdo_detail["tolov_usullar"]["naxt"]["active"]
                or daySavdo.savdo_detail["tolov_usullar"]["joyidaTolov"]["active"]
                or daySavdo.savdo_detail["tolov_usullar"]["depozit"]["active"]
                
            ):
                task_cashback_tushurish.delay(
                    savdo_id=daySavdo.daySavdo_nomer, shop_name=dokon.dokon_name
                )
            if (
                daySavdo.client_uuid is not None
                and bool( daySavdo.savdo_detail["hisobot"]["depozitga_tushgan_summa"]
                is not None or daySavdo.savdo_detail['tolov_usullar']['depozit']['active'])
            ):
                task_depozit_tushirish.delay(
                    savdo_id=daySavdo.daySavdo_nomer, shop_name=dokon.dokon_name
                )
            if daySavdo.product_arr is not None:
                serena_products(pk=daySavdo.pk , dokon_name=dokon.dokon_name)
            return JsonResponse(
                {"data": serialziers.data, "errors": False, "message": ""}, safe=False
            )
        except Exception as e:
            return JsonResponse({"data": None, "errors": True, "message": f"{e}"})

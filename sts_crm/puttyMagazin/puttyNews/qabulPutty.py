from datetime import date
from rest_framework.decorators import api_view
from rest_framework import status
from product.models import Product
from magazin.models import AllShop
from product.serenapath import serena_path
from .serialzier import VendorProductSerializer
from puttyMagazin.models import TavarPutty, DokonPutty
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from utills.productupdate import VendorProductsUpdate, ProductUpdate

from django.utils import timezone


@extend_schema(
    request=VendorProductSerializer, responses={201: VendorProductSerializer}
)
@api_view(["POST"])
def TavarPutty_Success(request):
    if request.method == "POST":
        serializer = VendorProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serenaPath = []
                send_magazin = None
                qabul_magazin = None
                putty_id = serializer.data.get("putty_id")
                putty = TavarPutty.objects.get(id=putty_id)
                status = serializer.data.get("putty_status")
                shop_id = putty.send_maagzinId
                dokon = AllShop.objects.get(id=shop_id)
                if not (putty.putty_status) and status:
                    if dokon.vendor:
                        print("hi")
                        if not(DokonPutty.objects.filter(dokon_uuid__id=shop_id).exists()):
                            vendor_dokon = DokonPutty.objects.create(dokon_uuid__id=dokon.pk)
                            vendor_dokon.save()
                        vendor_prod = VendorProductsUpdate(
                            products=putty.tavarlar, shop_id=shop_id
                        )
                    
                        vendor_prod.product__append
                    else:
                        dokon_prod = ProductUpdate(
                            products=putty.tavarlar, shop_id=shop_id
                        )
                        
                        dokon_prod.append_product
                    putty.putty_status = True
                    putty.save()

                    send_magazin = AllShop.objects.get(id=putty.shopId.pk).dokon_name
                    qabul_magazin = AllShop.objects.get(
                        id=putty.send_maagzinId
                    ).dokon_name
                    print("test")
                    for product in putty.tavarlar:
                        if product["product_serena"] is not None:
                            data = {
                                "product_id": product["product_id"],
                                "product_name": product["product_name"],
                                "material_nomer": product.get("material_nomer"),
                                "serena": product["product_serena"],
                                "path": {
                                    "yuboruvchi": f"{send_magazin}",
                                    "qabul_qiluvchi": f"{qabul_magazin}",
                                    "savdo_status":False,
                                    "putty_status": True,
                                    "vazvrat_status": False,
                                    "shartnoma": False,
                                    "clinet_id": "",
                                    "client_name": "",
                                    "date": f"{date.today()}",
                                    "date_time": f"{timezone.now().hour}:{timezone.now().minute}",
                                },
                            }
                            serenaPath.append(data)
                    if len(serenaPath):
                        serena_path(products=serenaPath)
                    return Response(
                        {"data": "success", "errors": False, "messsage": ""}
                    )
                if putty.putty_status:
                    return Response({"massage": "Sizda tavarni do'koningizda o'tgan"})
            except Exception as e:
                return Response({"data": None, "errors": True, "message": f"{e}"})
            else:
                return Response(
                    {"putty_status": False, "massage": "status o'zgartiring"}
                )
        return Response(serializer.errors)

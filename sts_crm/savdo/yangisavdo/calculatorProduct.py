from rest_framework.decorators import api_view
from rest_framework.views import APIView
from product.models import Product
from magazin.models import AllShop
from django.http import JsonResponse
from settings.models import SavdoSetting

# skidkaSetting=false , skidkaYoqish =false , tavar_skidka = false , dokonSettings_skidka


def skidka_funtion(shop_id):
    setting = SavdoSetting.objects.all().first()
    skidka_foiz = 0
    num = (
        AllShop.objects.get(id=shop_id).nastroyka is not None
        and float(AllShop.objects.get(id=shop_id).nastroyka.skidka)
        or 0
    )
    if setting.skidkaSetting:
        if setting.dokonSettings_skidka:
            skidka_foiz = (
                bool(num > (setting.skidka_max)) and num or float(setting.skidka_max)
            )
            return skidka_foiz
        else:
            return float(setting.skidka_max)
    else:
        return num


@api_view(["POST"])
def productCalculators_fun(request):
    if request.method == "POST":
        try:
            user = request.user
            products = request.data.get("products")
            shop_id = request.data.get("shop_id")
            umumiy_narx = 0
            skidka_narx = 0
            tavar_summasi = 0

            skidka = skidka_funtion(shop_id=shop_id)
            skida = skidka

            skidk = skidka_funtion(shop_id=shop_id)
            setting = SavdoSetting.objects.all().first()
            if setting.skidkaYoqish:
                if setting.tavar_skidka:
                    for i in products:
                        prod = Product.objects.get(id=i["product_id"])
                        if skidk <= prod.tavar_ckidka:
                            skidka = bool(skidk >= i["skidka"]) and i["skidka"] or skidk
                            skidka = skidka / 100
                        else:
                            skidka = (
                               bool(prod.tavar_ckidka >= i["skidka"])
                                and i["skidka"]
                                or prod.tavar_ckidka
                            )
                            skidka = skidka / 100
                        tavar_summasi = tavar_summasi + prod.price * i["count"]
                        umumiy_narx = (
                            umumiy_narx + (prod.price) * (1 - skidka) * i["count"]
                        )
                        skidka_narx = skidka_narx + prod.price * skidka * i["count"]
                    return JsonResponse(
                        {
                            "data": {
                                "tavarni_summasi": tavar_summasi,
                                "umumiy_narx": umumiy_narx,
                                "skidka_summa": skidka_narx,
                            },
                            "errors": False,
                            "message": "",
                        },
                        safe=False,
                    )

                else:

                    for i in products:
                        print(skidka)
                        prod = Product.objects.get(id=i["product_id"])

                        skidka = bool(skidk >= i["skidka"]) and i["skidka"]/100 or skidk/100
                        

                        if int(i['skidka']) ==0:
                            skidka = 0
                        else:
                            skidka =bool(int(i["skidka"]) < int(skidk)) and i["skidka"] or skidk
                        skidka = skidka / 100
                        tavar_summasi = tavar_summasi + prod.price * i["count"]
                        
                        umumiy_narx = (
                            umumiy_narx + (prod.price) * (1 - skidka) * i["count"]
                        )
                        skidka_narx = skidka_narx + prod.price * skidka * i["count"]
                    return JsonResponse(
                        {
                            "data": {
                                "tavarni_summasi": tavar_summasi,
                                "umumiy_narx": umumiy_narx,
                                "skidka_summa": skidka_narx,
                            },
                            "errors": False,
                            "message": "",
                        },
                        safe=False,
                    )
            else:
                for i in products:
                    prod = Product.objects.get(id=i["product_id"])
                    skidka = i["skidka"] and i["skidka"] or 0
                    skidka = skidka / 100
                    tavar_summasi = tavar_summasi + prod.price * i["count"]
                    umumiy_narx = umumiy_narx + (prod.price) * (1 - skidka) * i["count"]
                    skidka_narx = skidka_narx + prod.price * skidka * i["count"]

                return JsonResponse(
                    {
                        "data": {
                            "tavarni_summasi": tavar_summasi,
                            "umumiy_narx": umumiy_narx,
                            "skidka_summa": skidka_narx,
                        },
                        "errors": False,
                        "message": "",
                    },
                    safe=False,
                )
        except Exception as e:
            return JsonResponse({"data": None, "errors": True, "message": f"{e}"})

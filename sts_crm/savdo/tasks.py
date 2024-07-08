from celery import shared_task
from time import sleep
from product.serenapath import serena_path
from savdo.funtionViews.SavdoCashback import CashbackDataUpdate, HisobRaqam
from magazin.models import Savdo, DaySellerShop, Klient
from django.utils import timezone
from datetime import date


def _cashback_tushurish(savdo_id, shop_name):
    savdo = DaySellerShop.objects.get(daySavdo_nomer=savdo_id)
    telefon = int(Klient.objects.get(id=savdo.client_uuid.pk).client_user.phone)
    if (
        savdo.savdo_detail["tolov_usullar"]["joyidaTolov"]['active']
        or savdo.savdo_detail["tolov_usullar"]["naxt"]['active']
        or savdo.savdo_detail["tolov_usullar"]["plastik"]['active']
        or savdo.savdo_detail["tolov_usullar"]["depozit"]['active']
    ):
    # summa = savdo.savdo_detail['hisobot']['mahsulotUchun_tolov']
        summa = (
            float(savdo.savdo_detail["tolov_usullar"]["joyidaTolov"]["summa"]) / 100
            + float(savdo.savdo_detail["tolov_usullar"]["naxt"]["summa"]) / 100
            + float(savdo.savdo_detail["tolov_usullar"]["plastik"]["summa"]) / 100
            + float(savdo.savdo_detail["tolov_usullar"]["depozit"]['summa']/100)
        )

        cashback = CashbackDataUpdate(
            savdo_id=savdo_id,
            telefon=telefon,
            summa=summa,
            shop_name=shop_name,
            dokon=True,
        )
        savdo.savdo_detail["hisobot"]["tushgan_cashback_summa"] = summa
        savdo.save()
        cashback.cashback_tushurish
    if savdo.savdo_detail["hisobot"]['yechilgan_cashback_summa'] is not None:
        summa =  savdo.savdo_detail["hisobot"]['yechilgan_cashback_summa']
        cashback = CashbackDataUpdate(
            savdo_id=savdo_id,
            telefon=telefon,
            summa=summa,
            shop_name=shop_name,
            dokon=True,
        )
        cashback.cashback_yechish

    return None


def _depozit_tushurish(savdo_id, shop_name):

    savdo = DaySellerShop.objects.get(daySavdo_nomer=savdo_id)
    telefon = Klient.objects.get(id=savdo.client_uuid.pk).client_user.phone
    if (savdo.savdo_detail["hisobot"]["depozitga_tushgan_summa"]) is not None:
        summa = savdo.savdo_detail["hisobot"]["depozitga_tushgan_summa"]
        depozit = HisobRaqam(
            telefon=telefon,
            summa=summa,
            shop_name=shop_name,
            dokon=True,
            savdo_nomer=savdo.daySavdo_nomer,
        )
        depozit.hisob_tushurish
    if savdo.savdo_detail["tolov_usullar"]["depozit"]["active"]:
        summa = savdo.savdo_detail["tolov_usullar"]["depozit"]["summa"]
        depozit = HisobRaqam(
            telefon=telefon,
            summa=summa,
            shop_name=shop_name,
            dokon=True,
            savdo_nomer=savdo.daySavdo_nomer,
        )
        depozit.hisob_yechish
    return None


@shared_task
def task_cashback_tushurish(savdo_id, shop_name):
    sleep(3)
    _cashback_tushurish(savdo_id=savdo_id, shop_name=shop_name)
    return None

@shared_task
def task_depozit_tushirish(savdo_id, shop_name):
    sleep(4)
    _depozit_tushurish(savdo_id=savdo_id, shop_name=shop_name)



def _serena_path_product(pk, dokon_name):
    serenaPath = []
    daySavdo = DaySellerShop.objects.get(id=pk)
    for product in daySavdo.product_arr:
        if product["product_serena"] is not None:
                    data = {
                        "product_id": product["product_id"],
                        "product_name": product["product_name"],
                        "material_nomer": product["material_nomer"],
                        "serena": product["product_serena"],
                        "path": {
                            "yuboruvchi": dokon_name,
                            "qabul_qiluvchi": None,
                            "savdo_status":True,
                            "putty_status": False,
                            "vazvrat_status": False,
                            "shartnoma": False,
                            "clinet_id": daySavdo.client_uuid.pk,
                            "client_name": daySavdo.client_uuid.client_user.first_name,
                            "date": f"{date.today()}",
                            "date_time": f"{timezone.now().hour}:{timezone.now().minute}",
                        },
                    }
                    serenaPath.append(data)
    if len(serenaPath):
        serena_path(products=serenaPath)


@shared_task
def serena_products(pk, dokon_name):
    sleep(5)
    _serena_path_product(pk=pk, dokon_name=dokon_name)

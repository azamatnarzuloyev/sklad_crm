from product.models import (
    ProductSerenapathOne,
    ProductSerenapathTwo,
    ProductSerenapathFour,
    ProductSerenapathEnd,
    ZerenaPathStatus,
)
from datetime import date


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


def _binary_search(list, item):
    low = 0
    high = len(list) - 1
    while low <= high:
        mid = (low + high) // 2
        guess = list[mid]
        if guess == item:
            return mid
        if guess > item:
            high = mid - 1
        else:
            low = mid + 1
    return None


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


def serena_path() -> None:
    tekshirish = _tekshirish_fn()
    data = {
        "product_id": 251,
        "product_name": "kamera",
        "material_nomer": "sdsds232",
        "serena": ["ww167202", "uf135393", "UP160491"],
        "path": {"kamra": "dsdsds", "dsdsd": "dsdsd", "dsdsdds": "sdsddddsd"},
    }

    statment = _stetment_prod(tekshirish, data)

    return None


serena_path()

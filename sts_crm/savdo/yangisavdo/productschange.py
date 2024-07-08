from product.models import Product
from puttyMagazin.models import DokonPutty
from magazin.models import AllShop
from rest_framework.views import APIView


class ProductDataUpdateAll:
    def __init__(self, products: list, shop_id: str):
        self.products = products
        self.shop_id = shop_id

    @property
    def test_product_remove(self):
        arr = []
        for product in self.products:
            prod_test = Product.objects.get(id=product["product_id"])
            for i in prod_test.dokon_tavarlar:
                if str(i["id"]) == str(self.shop_id):
                    if i["array_serena"] is not None:
                        arr_serena = [
                            x
                            for x in set(product["product_serena"])
                            if x not in set(i["array_serena"])
                        ]
                        len(arr_serena) > 0 and arr.append(
                            {
                                "product_id": product["product_id"],
                                "product_serena": arr_serena,
                            }
                        ) or None
                    else:
                        product_count = (
                            i["product_count"] < product["product_count"]
                            and {
                                "product_id": product["product_id"],
                                "product_count": product["product_count"],
                            }
                            or None
                        )
                        if product_count is not None:
                            arr.append(product_count)
        return arr

    @property
    def remove_product(self):
        remove_test = self.test_product_remove
        if len(remove_test) > 0:
            return remove_test
        for product in self.products:
            prod_set = Product.objects.get(id=product["product_id"])
            for i in prod_set.dokon_tavarlar:
                if str(i["id"] == str(self.shop_id)):
                    if i["array_serena"] is not None:
                        i["array_serena"] = list(
                            set(i["array_serena"]) - set(product["product_serena"])
                        )
                        prod_set.save()
                    else:
                        i["product_count"] = (
                            int(i["product_count"]) - product["product_count"]
                        )
                        prod_set.save()
        return True

    @property
    def test_append_product(self):
        arr = []
        for product in self.products:
            prod_test = Product.objects.get(id=product["product_id"])
            for i in prod_test.dokon_tavarlar:
                if str(i["id"]) == str(self.shop_id):
                    if i["array_serena"]:
                        arr_serena = [
                            x
                            for x in set(product["product_serena"])
                            if x in set(i["array_serena"])
                        ]
                        data = (
                            len(arr_serena) > 0
                            and {
                                "product_id": product["product_id"],
                                "product_serena": arr_serena,
                            }
                            or None
                        )
                        if data is not None:
                            arr.append(data)
            return arr

    @property
    def append_product(self):
        appen_test = self.test_append_product
        if len(appen_test) > 0:
            return appen_test
        for product in self.products:
            prod_set = Product.objects.get(id=product["product_id"])
            for i in prod_set.dokon_tavarlar:
                if str(i["id"] == str("shop_id")):
                    if i["array_serena"] is not None:
                        i["array_serena"] = list(
                            set(i["array_serena"]) | set(product["product_serena"])
                        )
                        prod_set.save()
                    else:
                        i["product_count"] = int(i["product_count"]) + int(
                            product["product_count"]
                        )
                        prod_set.save()

        return True

{
    "product_id": {
        "product_name": "",
        "product_count": "",
        "product_serena": [],
        "product_image": [],
    }
}


class VendorProductUpdate:
    def __init__(self, products, shop_id):
        self.products = products
        self.shop_id = shop_id
        self.puttyproduct = DokonPutty.objects.get(dokon_uuid__id=shop_id)

    @property
    def product_test_remove(self):
        arr = []
        for product in self.products:
            if self.puttyproduct.tavarlar.get(product["product_id"]) is not None:
                if product["product_serena"] is not None:
                    arr_serena = [
                        x
                        for x in set(product["product_serena"])
                        if x
                        not in set(
                            self.puttyproduct.tavarlar[product["product_id"]][
                                "product_serena"
                            ]
                        )
                    ]
                    len(arr_serena) > 0 and arr.append(
                        {
                            "product_id": product["product_id"],
                            "product_serena": arr_serena,
                        }
                    ) or None
                else:
                    product_count = (
                        self.puttyproduct.tavarlar[product["product_id"]][
                            "product_count"
                        ]
                        < product["product_count"]
                        and {
                            "product_id": product["product_id"],
                            "product_count": product["product_count"],
                        }
                        or None
                    )
                    if product_count is not None:
                        arr.append(product_count)
            else:
                arr.append(
                    {
                        "product_id": product["product_id"],
                        "product_count": product["product_count"],
                        "product_serena": product["product_serena"],
                    }
                )
        return arr

    @property
    def remove_product(self):
        for product in self.products:
            if self.puttyproduct.tavarlar.get(product["product_id"]) is not None:
                if product["product_serena"] is not None:
                    self.puttyproduct.vendor_tavarlar[product["product_id"]][
                        "product_serena"
                    ] = list(
                        set(
                            self.puttyproduct.tavarlar[product["product_id"]][
                                "product_serena"
                            ]
                        )
                        - set(product["product_serena"])
                    )
                    self.puttyproduct.save()
                else:
                    self.puttyproduct.tavarlar[product["product_id"]][
                        "product_count"
                    ] = int(
                        self.puttyproduct.tavarlar[product["product_id"]][
                            "product_count"
                        ]
                    ) - int(
                        product["product_count"]
                    )
                    self.puttyproduct.save()
        return True

    @property
    def product_test_append(self):
        arr = []
        for product in self.products:
            if self.puttyproduct.tavarlar.get(product["product_id"]) is not None:
                if product["product_serena"] is not None:
                    arr_serena = [
                        x
                        for x in set(product["product_serena"])
                        if x
                        in set(
                            self.puttyproduct.tavarlar[product["product_id"]][
                                "product_serena"
                            ]
                        )
                    ]
                    len(arr_serena) > 0 and arr.append(
                        {
                            "product_id": product["product_id"],
                            "product_serena": arr_serena,
                        }
                    ) or None
            else:
                arr.append(
                    {
                        "product_id": product["product_id"],
                        "product_count": product["product_count"],
                        "product_serena": product["product_serena"],
                    }
                )
        return arr

    @property
    def product__append(self):
        for product in self.products:
            product_get = Product.objects.get(id=product["product_id"])
            if self.puttyproduct.tavarlar.get(product["product_id"]) is not None:
                if product["product_serena"] is not None:
                    self.puttyproduct.vendor_tavarlar[product["product_id"]][
                        "product_serena"
                    ] = list(
                        set(
                            self.puttyproduct.tavarlar[product["product_id"]][
                                "product_serena"
                            ]
                        )
                        | set(product["product_serena"])
                    )
                    self.puttyproduct.save()
                else:
                    self.puttyproduct.tavarlar[product["product_id"]][
                        "product_count"
                    ] = int(
                        self.puttyproduct.tavarlar[product["product_id"]][
                            "product_count"
                        ]
                    ) + int(
                        product["product_count"]
                    )
                    self.puttyproduct.save()
            else:
                self.puttyproduct.tavarlar[product["product_id"]] = {
                    "product_name": product_get.product_name,
                    "material_nomer": product_get.material_nomer,
                    "product_count": product["product_count"],
                    "product_serena": product["product_serena"],
                    "price": product_get.price,
                }
                self.puttyproduct.save()
        return True

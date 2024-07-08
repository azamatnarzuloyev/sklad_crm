from product.models import Product, TavarTekshiruv
from rest_framework.decorators import api_view
from .models import AllShop
from .serializers import CheckProductPUTSerialzier, ProductCheckSerialzier
from product.serializers import TavarTekshiruvSerialzier
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from product.pagination import CustomPagination

# tavarni listni chiqarish


@api_view(["GET"])
def tavar_tekshiruv(request):
    """
    body yuboradigan malumot
    {
    "shop_id": type(uuid);
    }
    """
    if request.method == "GET":
        shop_id = request.data.get("shop_id")
        if shop_id is None:
            return JsonResponse(
                {
                    "data": None,
                    "errors": True,
                    "message": "shop_id mavjud emas body shop_id yuboring",
                }
            )
        check: bool = (
            TavarTekshiruv.objects.filter(shop_id=shop_id).values("shop_id").exists()
        )
        if check:
            checkdata: bool = (
                TavarTekshiruv.objects.filter(shop_id=shop_id, status=False)
                .values("shop_id")
                .exists()
            )
            if checkdata:
                tekshiruv = TavarTekshiruv.objects.get(shop_id=shop_id, status=False)
                serialzier = TavarTekshiruvSerialzier(tekshiruv, many=False)
                return JsonResponse(
                    {"data": serialzier.data, "errors": False, "message": ""},
                    safe=False,
                )

            else:
                tekshiruv = TavarTekshiruv.objects.get(shop_id=shop_id, status=True)
                return JsonResponse(
                    {
                        "data": None,
                        "errors": True,
                        "message": "Bu do'kon tavarlarni takshirilgan . SIz yangi import malumotlarini ochishingiz kerak",
                        "date": f"{tekshiruv.create_at}",
                    },
                    safe=False,
                )
        else:
            return JsonResponse(
                {
                    "data": None,
                    "errors": True,
                    "message": "Bu do'kon tavarlarni import malumotlari mavjud emas",
                },
                safe=False,
            )


def _tekshiruv_create(shop_id, shop_name):
    products = Product.objects.raw(
        "SELECT id, material_nomer, price,  product_name, dokon_tavarlar FROM product_product ORDER BY id ASC"
    )
    product_data = []
    for product in products:
        for prod in product.dokon_tavarlar:
            if str(prod["id"]) == str(shop_id):
                if prod["product_count"] is None and len(prod["array_serena"]) > 0:
                    arr = {
                        "id": product.pk,
                        "price": product.price,
                        "product_name": product.product_name,
                        "material_nomer": product.material_nomer,
                        "product_count": prod["product_count"],
                        "product_serena": prod["array_serena"],
                        "present_count": None,
                        "present_serena": [],
                    }
                    product_data.append(arr)
                elif prod["array_serena"] is None and prod["product_count"] > 0:
                    arr = {
                        "id": product.pk,
                        "price": product.price,
                        "product_name": product.product_name,
                        "material_nomer": product.material_nomer,
                        "product_count": prod["product_count"],
                        "product_serena": prod["array_serena"],
                        "present_count": 0,
                        "present_serena": None,
                    }
                    product_data.append(arr)

    tavartekshirish = TavarTekshiruv()
    tavartekshirish.products = product_data
    tavartekshirish.shop_id = shop_id
    tavartekshirish.shop_name = shop_name
    tavartekshirish.save()
    return True


@api_view(["POST"])
def tekshiruvTavar_yaratish(request):
    """
    tekshiruv tavarlarini yaratish yangi import malumotlar ochish
    request: shop_id
    response: data: success
    """
    if request.method == "POST":
        shop_id = request.data.get("shop_id")
        if shop_id is None:
            return JsonResponse(
                {
                    "data": None,
                    "errors": True,
                    "message": "shop_id mavjud emas body shop_id yuboring",
                }
            )
        all_shop = AllShop.objects.get(id=shop_id)
        check: bool = (
            TavarTekshiruv.objects.filter(shop_id=shop_id).values("shop_id").exists()
        )
        if check:
            checkdata: bool = (
                TavarTekshiruv.objects.filter(shop_id=shop_id, status=False)
                .values("shop_id")
                .exists()
            )
            if not (checkdata):
                _tekshiruv_create(shop_id=shop_id, shop_name=all_shop.dokon_name)
                return JsonResponse({"data": "success", "errors": False, "message": ""})

            else:
                checkdataset = TavarTekshiruv.objects.get(shop_id=shop_id, status=False)
                return JsonResponse(
                    {
                        "data": None,
                        "errors": True,
                        "message": "import malumot yaratilgan",
                        "date": f"{checkdataset.create_at}",
                    }
                )
        else:
            _tekshiruv_create(shop_id=shop_id, shop_name=all_shop.dokon_name)
            return JsonResponse({"data": "success", "errors": False, "message": ""})


def _binary_search(list, lengs, item):
    low = 0
    high = lengs - 1
    while low <= high:
        mid = (low + high) // 2
        guess = list[mid]["id"]
        if guess == item:
            return mid
        if guess > item:
            high = mid - 1
        else:
            low = mid + 1
    return None


@api_view(["PUT"])
def tekshiruv_data_update(request):
    if request.method == "PUT":
        serialier = CheckProductPUTSerialzier(data=request.data)
        if serialier.is_valid():
            tekshiruvId = serialier.data.get("tekshiruvId")
            status = serialier.data.get("status")
            products = serialier.data.get("products")
            tekshiruv: bool = (
                TavarTekshiruv.objects.filter(id=tekshiruvId).values("id").exists()
            )
            if tekshiruv:
                tavar_tekshirish = TavarTekshiruv.objects.get(id=tekshiruvId)
                tavar_tekshirish.status = status
                tavar_tekshirish.save()
                lengs = len(TavarTekshiruv.objects.get(id=tekshiruvId).products)
                if products is not None:
                    for product in products:
                        prod_serialzier = ProductCheckSerialzier(data=product)
                        if prod_serialzier.is_valid():
                            present_count = prod_serialzier.data.get("present_count")
                            present_serena = prod_serialzier.data.get("present_serena")
                            id = prod_serialzier.data.get("id")
                            data_index = _binary_search(
                                list=list(tavar_tekshirish.products).sort(),
                                lengs=lengs,
                                item=id,
                            )
                            if tavar_tekshirish.products[data_index]["id"] == id:
                                tavar_tekshirish.products[data_index][
                                    "present_serena"
                                ] = present_serena
                                tavar_tekshirish.products[data_index][
                                    "present_count"
                                ] = present_count
                                tavar_tekshirish.save()
                        else:
                            return JsonResponse(
                                {
                                    "data": None,
                                    "errors": True,
                                    "message": prod_serialzier.errors,
                                },
                                safe=False,
                            )
                    return JsonResponse(
                        {
                            "data": "update",
                            "errors": False,
                            "message": "",
                        },
                        safe=False,
                    )
                dataset = TavarTekshiruvSerialzier(tavar_tekshirish, many=False)
                return JsonResponse(
                    {
                        "data": dataset.data,
                        "errors": False,
                        "message": "",
                    },
                    safe=False,
                )
        return JsonResponse(
            {
                "data": None,
                "errors": True,
                "message": serialier.error_messages,
                "detail": serialier.errors,
            }
        )


class TavarTekshiruvVIews(ListAPIView):
    queryset = TavarTekshiruv.objects.all()
    serializer_class = TavarTekshiruvSerialzier
    pagination_class = CustomPagination

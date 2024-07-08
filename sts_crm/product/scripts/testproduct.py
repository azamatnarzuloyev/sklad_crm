from product.models import Product, TavarTekshiruv

item = "dbc60ded-7282-447f-bb7f-4e77a9aafbb2"
from time import sleep, perf_counter


def binary_search(list, item):
    low = 0
    high = Product.objects.count() - 1
    while low <= high:
        mid = (low + high) // 2
        guess = list[mid].pk
        if guess == item:
            return mid
        if guess > item:
            high = mid - 1
        else:
            low = mid + 1
    return None


def run():
    data = list(
        Product.objects.raw(
            "SELECT id, material_nomer, price,  product_name, dokon_tavarlar FROM product_product ORDER BY id ASC"
        )
    )

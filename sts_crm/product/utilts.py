from .models import Product, ProductJsonArxiv

from datetime import date 


def product_arxiv_funtions():
    data_set = []
    if not(ProductJsonArxiv.objects.filter(date=date.today()).exists()):
        data_product = Product.objects.raw("SELECT id, material_nomer, price,  product_name, dokon_tavarlar FROM product_product ORDER BY id ASC")
        for i in data_product:
            data = {
                "product_name": i.product_name,
                "material_nomer": i.material_nomer,
                "price": i.price,
                "dokon_tavarlar": i.dokon_tavarlar
            }
            data_set.append(data)

        product_json = ProductJsonArxiv.objects.create(
            date = date.today(),
            json_product = data_set
        )
        product_json.save()







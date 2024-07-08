from puttyMagazin.models import TavarPutty  , DokonPutty
from django.db.models.query import QuerySet
from django.db import connection
from product.models import Product

def run():
    tavar = DokonPutty.objects.first()
    data = []
    for i in tavar.tavarlar:
        for i in tavar.tavarlar:
            data.append({
                "product_id": i,
                "product_name": tavar.tavarlar[i]['product_name'],
                "product_serena": tavar.tavarlar[i]['product_serena']
                
            })

    print(data[0])
    

    



 








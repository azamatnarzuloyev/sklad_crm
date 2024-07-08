from product.models import Product
from puttyMagazin.models import DokonPutty
from magazin.models import AllShop
from rest_framework.response import Response

def testSavdo_product(i, shop_id):
        errors_serena = []
        if i['product_serena'] is not None:
            product = Product.objects.get(id=i['id'])
            for s in product.dokon_tavarlar:
                if s['id'] ==str(shop_id):
                    for j in i['product_serena']:
                        if j in s['array_serena']:
                             pass
                         
                        else:
                            errors_serena.append(j)
                       
                           
            if errors_serena:
                    return ({
                        "product_id": product.id,
                        "errors": True,
                        "masage": errors_serena,
                    })
            else:
                    return ({
                        "errors": False,
                    })
        else:
            product = Product.objects.get(id=i['id'])
            for s in product.dokon_tavarlar:
                if s['id'] == str(shop_id):
                
                    if int(s['product_count']) > int(i['product_count']):
                        
                        s['product_count'] = s['product_count'] - i['product_count']  
                    else:
                        errors_serena.append(i['product_count'])
            if errors_serena:
                return ({
                        "product_id": product.id,
                        "errors": True,
                        "masage": errors_serena,

                    })
            else:
                return ({
                    "errors": False
                })


def removeSavdo_product(i, shop_id):
        if i['product_serena'] is not None:
            product = Product.objects.get(id=i['id'])
            for j in i['product_serena']:
                for s in product.dokon_tavarlar:
                    if s['id'] == str(shop_id):
                            s['array_serena'].remove(j)
                            product.save()     
        else:
            product = Product.objects.get(id=i['id'])
            for s in product.dokon_tavarlar:
                if s['id'] == shop_id:
                        s['product_count'] = s['product_count'] - i['product_count']
                        product.save()
                  

def _vendorDokonTest(shop):
    try:
        return DokonPutty.objects.get(dokon_uuid__id=shop)
    except:
        return None


def vendorSavdo_products(shop, productarr):
    vendor_product = _vendorDokonTest(shop=shop)
    errors = []
    if vendor_product:
        for i in vendor_product.tavarlar:
            if i['id'] == productarr['id'] and productarr['product_serena']:
                for j in productarr['product_serena']:
                    if j in i['product_serena']:
                        pass
                    else:
                        errors.append(j)
            
            if i['id'] == productarr['id'] and productarr['product_count']:
                if i['product_count'] >= productarr['product_count']:
                    pass
                else:
                    errors.append(productarr['product_count'])
        if errors:
            return ({
                "errors": True,
                "product_id": productarr['id'],
                "massage": errors
            })
        else:
            return ({
                "errors": False
            })

def vendorSavdo_products_remove(shop, productarr):
    if DokonPutty.objects.filter(dokon_uuid__id=shop).exists():
        vendor_product =DokonPutty.objects.get(dokon_uuid__id=shop)
    else:
        return Response({"errors": "product not fount"})
    if vendor_product:
        for i in vendor_product.tavarlar:
            if i['id'] == productarr['id'] and productarr['product_serena']:
                for j in productarr['product_serena']:
                    i['product_serena'].remove(j)
                    vendor_product.save()
            if i['id'] == productarr['id'] and productarr['product_count']:
                i['product_count'] = int(i['product_count']) -  int(productarr['product_count'])
                vendor_product.save()
            
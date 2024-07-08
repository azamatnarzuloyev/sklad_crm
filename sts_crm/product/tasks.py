# from celery import shared_task
# from product.utilts import product_arxiv_funtions
# from .models import Product, ProductJsonArxiv
# from datetime import date


# @shared_task
# def productJsonTask():
#     arxiv_bool: bool = ProductJsonArxiv.objects.filter(date=date.today()).exists()
#     if not (arxiv_bool):
#         product_arxiv_funtions()
#         print("success")
#     print("product json update")



# @shared_task
# def task_productPath():
#     pass 

from django.urls import path
from .views import (product_detail  , import_product , import_data_get)

from product.newData.views import  product_shop , product_update_views
from product.manyproductgetorpost.productviews import product_update_funtion , new_productpost_funtion
from .savdoproduct import ProductSavdoViews
from .serenapath import SerenaPathViews

urlpatterns = [
    path('product-data/<int:pk>/', product_detail, name='product-data'),
    path('product-dokon/', product_shop , name='dokon'),
    path('product-update-view/<int:pk>/', product_update_views , name='product-update-view'),
    # yangi product urls 
    path('import-product/', import_product , name="import-product"),
    path('import-data-get/' , import_data_get , name="import-data-get"),
    path('product-update-data/', product_update_funtion , name='product-update-funtion'),
    path('product-data/', new_productpost_funtion , name='product-post-funtion'),
    # analiz
    path('product-savdo/<int:pk>/', ProductSavdoViews.as_view(), name='savdo-product'),
    path('serena-path/', SerenaPathViews.as_view()),
]

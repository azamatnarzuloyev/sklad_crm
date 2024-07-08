from django.urls import path

from savdo.funtionViews.TashkilotViews import tashkilot_funtion
from .views import  client_create, userData_update 
from .clientverify import client_verify_view

from savdo.funtionViews.ustanofka import ustanofka_xodimlar, servis_funtion
from savdo.funtionViews.OrderClient import GeneratePdf , render_pdf_view , savdo_getApiViews_pdf
from .news_savdo import client_get_or_create , client_data_updated_funtion , client_cashback_or_hamyon
from savdo.yangisavdo.views import SavdoCreateViews
from savdo.yangisavdo.calculatorProduct import productCalculators_fun
from savdo.yangisavdo.getsavdo import DokonSavdoViews

urlpatterns = [
    # path('client-get-or-create/', client_create , name='client-get'),
    path('client-verify/', client_verify_view, name='client-verify-view'),
    # path('client-data-update/', userData_update, name='client-update'),
    path('client-get-or-create/',client_get_or_create , name='client-get-or-create' ),
    path('client-data-update/', client_data_updated_funtion , name="client-data-update"),
    # ustanofka xizmat
    path('ustanofka-xodimlar/', ustanofka_xodimlar , name='ustanofka-xodimlar'),
    path('ustanofka-xodimlar/<int:pk>/', ustanofka_xodimlar , name='ustanofka-xodimlar'),
    path('servis-xizmat/', servis_funtion , name='servis-xizmat'),
    path('servis-xizmat/<int:pk>/', servis_funtion , name='servis-xizmat'),
    # tashkilot
    path('tashkilot-yaratish/', tashkilot_funtion, name='tashkilot-yaratish'),
    # pdf
    path('pdf-file/', GeneratePdf.as_view(), name='pdf-file'),
    path('pdf/', render_pdf_view, name='pdf'),
    path('savdo-all-pdf/', savdo_getApiViews_pdf , name='savdo-pdf-views'),
    # yangi savdo 
    path('yangi-savdo/', SavdoCreateViews.as_view()),
    path('savdo-calculator/', productCalculators_fun , name='savdo-calculator'),
    path('get-yangi-savdo/', DokonSavdoViews.as_view(), name='yangi-savdo-get'),
    path('validate-cashback-depozit/', client_cashback_or_hamyon , name='validate-cashback-depozit'),
]


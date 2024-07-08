from django.urls import path
from .viewsall import get_hamyon, update_hamyon, KardListUpdateViews,KartListRetriveupdate 
from .views import HamyonListViews , mobile_savdolar , site_savdo_get , request_dataset
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [

    path('karta-update/<str:pk>/',KartListRetriveupdate.as_view(), name="karta-update"),
    path('karta-list/', KardListUpdateViews.as_view(),name='karta-list'),
    path('hamyon/', HamyonListViews.as_view(), name='hamyon-list-create'),
    path('hamyon/<int:pk>/update/', update_hamyon, name='posts-update'),
    path('hamyon/<int:pk>/', get_hamyon, name='posts-get'),
    path('mobile-all-savdo/', mobile_savdolar , name='mobile-all-savdo'),
    path('site-savdo-get/<str:phone>/', site_savdo_get , name='site-savdo-get'),
    path('data-set/', request_dataset),
]


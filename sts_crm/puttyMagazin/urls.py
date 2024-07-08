from django.urls import path
from puttyMagazin.puttyNews.views import TavarPuttyApiviews, TavarPuttyDetailApiviews, VendorProductViews, PuttyViews, DokonPuttyGet
from puttyMagazin.puttyNews.qabulPutty import TavarPutty_Success
from puttyMagazin.puttyNews.deletePutty import DeletePuttyViews
from puttyMagazin.puttyNews.zakasproduct import zakasProduct_funtion
from .views import DokonPuttyViews
urlpatterns = [
    path('putty-get-or-post/', TavarPuttyApiviews.as_view(), name='putty-news'),
    # path('putty-get-or-post/<str:pk>/', TavarPuttyApiviews.as_view(), name='putty-news'),
    path('putty-get/', DokonPuttyGet.as_view(), name='putty-get'),
    path('putty-get-or-post/<str:pk>/', TavarPuttyDetailApiviews.as_view(), name='putty-news'),
    path('vendor-product/',VendorProductViews.as_view(), name='vendor-product' ),
    path('putty-qabul/', TavarPutty_Success , name='putty-qabul'),
    path('putty-delete/', DeletePuttyViews.as_view() , name='putty-delete'),
    path('test-url/', PuttyViews.as_view(), name='test-product'),

    # zakas product
    path('zakas-product-putty/',zakasProduct_funtion , name='zakas-product-putty' ),
    path('vendor-prod/', DokonPuttyViews.as_view()),
]

from django.urls import path
from .views import DokonCreateView, DokonLogin, DokonlistVIew
from .clientGet import client_get, hamfonFilter
from .checkproduct import tavar_tekshiruv , tekshiruvTavar_yaratish , tekshiruv_data_update , TavarTekshiruvVIews
urlpatterns = [
    path('dokon-get-or-create/', DokonCreateView.as_view(), name='dokon-get-or-create'),
    path('dokon-login/', DokonLogin.as_view(), name='dokon-login'),
    path('dokon-login-get/<int:userId>/', DokonLogin.as_view(), name='dokon-login'),
    path('dokon-list/<int:userId>/', DokonlistVIew.as_view(), name='dokon-list'),
    path('dokon-list/', DokonlistVIew.as_view(), name='dokon-list'),
    path('client-get/', client_get, name='client-get'),
    path('hamyon-post-phone/', hamfonFilter , name='hamyon'),
    # news 
    path('dokontavar-verify-get/', tavar_tekshiruv, name='dokon-tavar-tekshiruv'),
    path('dokontavar-verify-post/', tekshiruvTavar_yaratish , name='tekshiruv-yaratish'),
    path('dokontavar-verify-update/', tekshiruv_data_update , name='tekshiruv-upate'),
    path('dokontavar-verify-all/', TavarTekshiruvVIews.as_view() , name='tekshiruv-upate'),
]

from django.urls import path

from account.mobileLogin import MobileDOkonVerifyOtp, MobileLoginViews
from .views import mobile_product_list , dokon_savdo_funtion
from .dikinList import allshop_user_funtion
urlpatterns = [
    path('mobile-login/', MobileLoginViews.as_view(), name='mobile-login'),
    path('mobile-verify/', MobileDOkonVerifyOtp.as_view(), name='mobile-verify'),
    path('mobile-product-list/', mobile_product_list , name='mobile-product-list'),
    path('mobile-get-savdo/', dokon_savdo_funtion , name='mobile-get-savdo'),
    path('dokon-list-user/', allshop_user_funtion , name='dokon-list-user' )
]

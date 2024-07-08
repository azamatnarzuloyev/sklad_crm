from django.urls import path
from .views import SrmUserModelViews , goust_userFuntion , goust_PostFuntion

urlpatterns = [
    path('srm-user/', SrmUserModelViews.as_view() , name='srm-users'),
    path('crm-goust/', goust_userFuntion , name='goust'),
    path('crm-goust-post/', goust_PostFuntion , name='goust-post-fun'),
]


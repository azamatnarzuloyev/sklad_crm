from django.urls import path
from .views import Category_views

urlpatterns = [
    path('category-views/', Category_views , name='category-views'),
]


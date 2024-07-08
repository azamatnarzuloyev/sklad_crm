from django.urls import path
from .views import ListPostviews, home_cache, post_tasks 


urlpatterns = [
    path('get-post/', ListPostviews.as_view(), name='get-post'),
    path('cache-home/', home_cache),
    path('test-redis/', post_tasks)
]
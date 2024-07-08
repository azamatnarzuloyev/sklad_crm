from __future__ import annotations
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)



urlpatterns = [

    # global url
    path('admin/', admin.site.urls),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    # api documentation authentication 
    path('api/account/', include('account.urls', namespace='account')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path("__debug__/", include("debug_toolbar.urls")),

  # cashback url
    path('api/card/', include('cash.urls')),
    path('api/post/', include('post.urls')),

    # crm urls 
    path('crm/', include('product.urls')),
    path('crm/', include('magazin.urls')),
    path('crm/', include('puttyMagazin.urls')),
    path('crm/', include('savdo.urls')),
    path('crm/', include('category.urls')),
    path('crm/' , include('crmuser.urls')),

    # mobile urls
    path('mobile/', include('mobileApp.urls')),
    
    
]

# add root static files
urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
        )
# add media static files
urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
        )

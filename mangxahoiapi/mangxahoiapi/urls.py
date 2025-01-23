"""
URL configuration for mangxahoiapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from mangxahois.views import (
    UserViewSet, BaiDangViewSet, BinhLuanViewSet, ReactionViewSet,
    user_stats_api, get_available_years
)
from mangxahois.admin import admin_site
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Khai báo schema cho Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Mạng Xã Hội API",
        default_version='v1',
        description="API documentation for Mạng Xã Hội project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

# Định nghĩa router cho DRF ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'baidang', BaiDangViewSet, basename='baidang')
router.register(r'binhluan', BinhLuanViewSet, basename='binhluan')
router.register(r'reactions', ReactionViewSet, basename='reactions')

urlpatterns = [
    # Các API chính
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
    path('user-stats-api/', user_stats_api, name='user_stats_api'),
    path('get-available-years/', get_available_years, name='get_available_years'),

    # API documentations
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # CKEditor
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # OAuth2 authentication
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

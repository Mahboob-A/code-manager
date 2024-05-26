"""
URL configuration for code_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework.permissions import AllowAny

# service documentation
doc_schema_view = get_schema_view(
    openapi.Info(
        title="Code Manager API",
        default_version="v1.0",
        description="API Endpoints for Code Manger Service of AlgoCode Platform",
        contact=openapi.Contact(email="iammahboob.a@gmail.com"),
        license=openapi.License(name="MIT Licence"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    path("redoc/", doc_schema_view.with_ui("redoc", cache_timeout=0)),
    path(settings.ADMIN_URL, admin.site.urls),
    
    # code_display app urls 
    path("api/v1/problems/", include("core_apps.code_display.urls")),
 
    # code_submit app urls    
    path('api/v1/code/', include('core_apps.code_submit.urls')), 
    
    # code_result app urls 
    path('api/v1/result/', include('core_apps.code_result.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Code Manager Service API"
admin.site.site_title = "Code Manager Service Admin Portal"
admin.site.index_title = "Welcome to Code Manager Service API Portal"

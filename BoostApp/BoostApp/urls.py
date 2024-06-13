"""
URL configuration for BoostApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version=f"v{settings.API_VERSION}",
        description=" ",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f"api/v{settings.API_VERSION}/user/", include("user_app.urls")),
    path(f"api/v{settings.API_VERSION}/games/", include("games_app.urls")),
    path(f"api/v{settings.API_VERSION}/divisions/", include("divisions_app.urls")),
    path(f"api/v{settings.API_VERSION}/boosting_requests/", include("boosting_request_app.urls")),
    path(f"api/v{settings.API_VERSION}/reviews/", include("reviews_app.urls")),
    path(f"api/v{settings.API_VERSION}/chat/", include("chat_app.urls")),
    path(f"api/v{settings.API_VERSION}/chat_info/", include("chat_app.http_urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

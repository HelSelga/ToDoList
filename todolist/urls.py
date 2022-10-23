"""todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from todolist import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name='schema'),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name='schema')),
    path("‹oauth_path›/", include("social_django.urls", namespace="social")),
    # path("auth/", include('rest_framework.urls')),
    # path('api/token/', TokenObtainPairView.as_view(), name='token'),
    # path('api/refresh/', TokenRefreshView.as_view(), name='refresh token'),
    # path("core/", include("core.urls")),
    # path("goals/", include("goals.urls")),
    # path("bot/", include("bot.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

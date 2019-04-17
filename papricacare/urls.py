"""papricacare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from drug import viewsets
import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'prod', viewsets.ProdViewSet)
router.register(r'regi', viewsets.RegiViewSet)
router.register(r'ingre', viewsets.IngreViewSet)
router.register(r'form', viewsets.FormViewSet)
router.register(r'desc', viewsets.DescViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drug/', include('drug.urls')),
    path('hospital/', include('hospital.urls')),
    path('disease/', include('disease.urls')),
    path('ocr/', include('ocr.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.HomeView.as_view(), name='home'),
    path('chat/', include('chat.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]
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
import views
from rest_framework import routers, serializers, viewsets
import drug

# Serializers define the API representation.
class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = drug.models.Product
        fields = ('__all__')

class RegiSerializer(serializers.ModelSerializer):
    class Meta:
        model = drug.models.Registration
        fields = ('__all__')

class IngreSerializer(serializers.ModelSerializer):
    class Meta:
        model = drug.models.Ingredient
        fields = ('__all__')

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = drug.models.IngreForm
        fields = ('__all__')
        
class DescSerializer(serializers.ModelSerializer):
    class Meta:
        model = drug.models.IngreDesc
        fields = ('__all__')
        
# ViewSets define the view behavior.
class DrugViewSet(viewsets.ModelViewSet):
    queryset = drug.models.Product.objects.all()
    serializer_class = DrugSerializer
    
class RegiViewSet(viewsets.ModelViewSet):
    queryset = drug.models.Registration.objects.all()
    serializer_class = RegiSerializer
    
class IngreViewSet(viewsets.ModelViewSet):
    queryset = drug.models.Ingredient.objects.all()
    serializer_class = IngreSerializer
    
class FormViewSet(viewsets.ModelViewSet):
    queryset = drug.models.IngreForm.objects.all()
    serializer_class = FormSerializer
    
class DescViewSet(viewsets.ModelViewSet):
    queryset = drug.models.IngreDesc.objects.all()
    serializer_class = DescSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'drug', DrugViewSet)
router.register(r'regi', RegiViewSet)
router.register(r'ingre', IngreViewSet)
router.register(r'form', FormViewSet)
router.register(r'desc', DescViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drug/', include('drug.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.HomeView.as_view(), name='home'),
    path('chat/', include('chat.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]

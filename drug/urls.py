from django.urls import path
from django.views import generic
from drug import views 

app_name = 'drug'

urlpatterns = [    
    path('', generic.TemplateView.as_view(template_name='drug/index.html'), name='index'),
    path('<int:product_code>/api/', views.APIView.as_view(), name='api'),
]
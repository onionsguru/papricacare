from django.urls import path
from django.views import generic
from ocr import views

app_name = 'ocr'

urlpatterns = [    
    path('', generic.TemplateView.as_view(template_name='ocr/index.html'), name='index'),
    path('get/', views.GetView.as_view(), name='get'),
    path('get_rest', views.GetRestView.as_view(), name='get_rest'),
]
from django.urls import path
from django.views import generic

app_name = 'drug'

urlpatterns = [    
    path('', generic.TemplateView.as_view(template_name='drug/index.html'), name='index'),
]
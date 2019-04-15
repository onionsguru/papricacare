from django.urls import path
from django.views import generic
from drug import views, viewsets
from rest_framework import routers
from django.urls import path, include

app_name = 'drug'

urlpatterns = [    
    path('', generic.TemplateView.as_view(template_name='drug/index.html'), name='index'),
    path('<str:table>/<str:col>/json/', views.APIView.as_view(), name='api'),
    path('<str:name>/name/', viewsets.DrugNameViewSet.as_view()),
]
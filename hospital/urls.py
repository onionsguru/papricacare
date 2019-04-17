from django.urls import path
from django.views import generic
from hospital import views
from django.urls import path, include

app_name = 'hospital'

urlpatterns = [    
    path('<str:table>/<str:col>/json/', views.APIView.as_view(), name='api'),
]
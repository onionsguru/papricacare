from django.urls import path
from chat import views

app_name = 'chat'

urlpatterns = [    
    path('', views.IndexView.as_view(), name='index'),
    path('join/', views.IndexView.as_view(), name='join'),
    path('<str:msg>/join/', views.IndexView.as_view(), name='join'),
    path('open/', views.OpenView.as_view(), name='open'),
    path('<str:error_msg>/enter/', views.EnterView.as_view(), name='enter'),    
    path('<int:pk>/<int:chatter_id>/enter/', views.EnterView.as_view(), name='enter'),
    path('<int:pk>/<int:chatter_id>/talk/', views.TalkView.as_view(), name='talk'),
]

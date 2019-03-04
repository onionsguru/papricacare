from django.urls import path
from chat import views

app_name = 'chat'

from chat import models

models.Chatroom.objects.all().delete()  # clear all chatrooms that could remain becasue of abnormal termination

urlpatterns = [    
    path('', views.IndexView.as_view(), name='index'),
    path('join/', views.IndexView.as_view(), name='join'),
    path('<str:msg>/join/', views.IndexView.as_view(), name='join'),
    path('open/', views.OpenView.as_view(), name='open'),
    path('<str:error_msg>/enter/', views.EnterView.as_view(), name='enter'),    
    path('<int:pk>/<int:chatter_id>/enter/', views.EnterView.as_view(), name='enter'),
    path('<int:pk>/<int:chatter_id>/talk/', views.TalkView.as_view(), name='talk'),
]
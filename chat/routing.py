# chat/routing.py
from django.conf.urls import url
#from . import consumers
from chat import comm

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_id>[^/]+)/(?P<user_id>[^/]+)/$', comm.ChatChannel),
]
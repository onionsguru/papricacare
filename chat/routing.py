# chat/routing.py
from django.conf.urls import url
#from . import consumers
from chat.comm import ChatChannel
from ocr.comm import OcrChannel

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_id>[^/]+)/(?P<user_id>[^/]+)/$', ChatChannel),
    url(r'^ws/ocr/$', OcrChannel),
]
from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync
import json
from chat import models
import datetime
import pytz
from papricacare.ocr import ocr
import io

class ChatChannel(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_id = 'chat_%s' % self.room_id
        
        user = models.User.objects.all().get(pk=self.user_id)        
        cur_time = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
        time_text = str(cur_time)
        message = f'<b>{user.nickname_text}</b> has joined at <{time_text[:19]}>'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_id,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'chat_message',
                'message': message,
                'img_src': '#'
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
 
        user = models.User.objects.all().get(pk=self.user_id)        
        message = f' <b>{user.nickname_text}</b> has left!'
        is_owner = user.is_owner
        user.delete()     
        
        ch = models.Chatroom.objects.all().get(pk=self.room_id)
        if ch.user_set.count() == 0:
            ch.delete()
        elif is_owner:
            u = ch.user_set.first();
            u.is_owner = True 
            u.save()
       
        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'chat_message',
                'message': message,
                'img_src': '#'
            }
        )
        
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )
 
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        try:
            message = text_data_json['message']
            user_id = text_data_json['user']
            attr = text_data_json['attr']
            
            user = models.User.objects.all().get(pk=user_id)
            message = f'<b>{user.nickname_text}</b> : {message}'
    
            if attr['img_src'] != '#' and \
                (attr['is_privacy'] or attr['is_num'] or attr['is_char'] or\
                 attr['is_drug'] or attr['is_disease'] or attr['is_hosp']):
                (candidates, attr['img_src']) = ocr.process(attr)
                if attr['is_drug']:
                    message = message + '<br>' + str(candidates)
        except KeyError:
            message = 'a wrong request'
            attr = dict()
            attr['img_src'] = '#'  
            print(f'# error of {message}: "{text_data_json}"')
                         
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'chat_message',
                'message': message,
                'img_src': attr['img_src']
            }
        )
            
    def get_chatters(self, id):
        chatroom = models.Chatroom.objects.all().get(pk=id)
        chatter_list = []
        
        for u in chatroom.user_set.all():
            if u.auth_name != '':         
                if u.is_owner:
                    chatter_list.append('<b>' + u.nickname_text+ ' (' + u.auth_name + ')</b>&nbsp;&#9819;<br>')
                else:
                    chatter_list.append(u.nickname_text+' (' + u.auth_name + ')<br>')
            else:
                if u.is_owner:
                    chatter_list.append('<b>' + u.nickname_text + '</b>&nbsp;&#9819;<br>')
                else:
                    chatter_list.append(u.nickname_text+'<br>')
        return chatter_list
      
    # Receive message from room group
    async def chat_message(self, event):
        event['chatter_list'] = self.get_chatters(self.room_id)

        # Send message to WebSocket
        await self.send(json.dumps(event))

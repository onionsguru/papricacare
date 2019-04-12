from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync
import json
from papricacare.ocr import ocr
import io

class OcrChannel(AsyncWebsocketConsumer):
    id  = 0
    async def connect(self):
        OcrChannel.id += 1
        self.room_group_id = 'ocr_%s' % OcrChannel.id
     
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_id,
            self.channel_name
        )

        await self.accept()
        print(f'ocr websocket connected:{OcrChannel.id}')

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )
 
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = None
        try:
            attr = text_data_json['attr']
            if attr['img_src'] != '#' and \
                 (attr['is_privacy'] or attr['is_num'] or attr['is_char'] or\
                 attr['is_drug'] or attr['is_disease'] or attr['is_hosp']):
                (candidates, attr['img_src']) = ocr.process(attr)
                if attr['is_drug']:
                    message = str(candidates)
        except KeyError as detail:
            message = 'a wrong request' + detail.args[0] 
            attr = dict()
            attr['img_src'] = '#'  
            text_data_json['attr']['img_src'] = '#'
            print(f'# error of {message}: "{text_data_json}"')
                         
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'ocr_message',
                'message': message,
                'img_src': attr['img_src']
            }
        )
         
    # Receive message from room group
    async def ocr_message(self, event):
        # Send message to WebSocket
        text_data=json.dumps({
            'message': event['message'],
            'img_src': event['img_src'],
        })
        await self.send(text_data)

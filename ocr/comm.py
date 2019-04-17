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
        drugs, disease_name, hospital_name, issue_date = [], '', '', ''

        try:
            attr = text_data_json['attr']
            if attr['img_src'] != '#' and \
                 (attr['is_privacy'] or attr['is_num'] or attr['is_char'] or\
                 attr['is_drug'] or attr['is_disease'] or attr['is_hosp']):
                (disease_name, hospital_name, issue_date, drugs, attr['img_src']) = ocr.process(attr)
        except KeyError as detail:
            drugs = ['wrong request',]
            attr = dict()
            attr['img_src'] = '#'  
            text_data_json['attr']['img_src'] = '#'
                         
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'ocr_message',
                'message': { 'drugs': drugs, 'diseases': disease_name, 'hospital':hospital_name, 
                    'issue': issue_date },
                'img_src': attr['img_src']
            }
        )
         
    # Receive message from room group
    async def ocr_message(self, event):
        # Send message to WebSocket

        '''
        # Test data
        event['message'] = {
                'disease' : '통풍',
                'hospital' : '삼성병원',
                'issue' : '2018-04-03',
                'drugs':[{'reg_code': '644304080', 'drug_name': '콜킨정(콜키신)', 'dose':'1', 'qty_perday':'3'}, 
                    {'reg_code': '644704010', 'drug_name': '페브릭정40밀리그램(페북소스타트)', 'dose':'2', 'qty_perday':'2'}]}
        '''

        print(event['message'])
        await self.send(json.dumps(event))

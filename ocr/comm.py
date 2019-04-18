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
        drugs, disease_name, hospital_name, issue_date, serial_info = [], '', '', '', ''

        try:
            attr = text_data_json['attr']
            if attr['img_src'] != '#' and \
                 (attr['is_privacy'] or attr['is_num'] or attr['is_char'] or\
                 attr['is_drug'] or attr['is_disease'] or attr['is_hosp']):
                (serial_info, disease_name, hospital_name, date, drugs, attr['img_src']) = ocr.process(attr)
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
                    'dates': date, 'serial': serial_info },
                'img_src': attr['img_src'],
                'is_test': attr['is_test']
            }
        )
         
    # Receive message from room group
    async def ocr_message(self, event):
        # Send message to WebSocket

        if event['is_test']:
            event['message'] = {"drugs":[{"prod_code":"648900560","drug_name":"쎄레브렉스캡슐200밀리그램(세레콕시브)","dose":"-","qty_perday":"-"}],"diseases":[{"code":"M19.99","name":"상세불명의 관절증, 상세불명 부분"},{"code":"K10.2","name":"턱의 염증성 병태"}],"hospital":{"name":"학교법인가톨릭학원가톨릭대학교서울성모병원"},
            "dates":[{"issue":"2019/04/17"},{"issue":"2019-04-24"},{"issue":"2019-04-17"}], 'serial': '740514'}       

        print(event['message'])
        await self.send(json.dumps(event))

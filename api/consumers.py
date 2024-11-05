import json
from channels.generic.websocket import AsyncWebsocketConsumer
from uuid import UUID

class SMReadingsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("sensor_readings",self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("sensor_readings",self.channel_name)

    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            "sensor_readings",
            {
                'type' : 'sensor_reading_message',
                'message' : message
            }
        )

    async def sensor_reading_message(self,event):
        message = event['message']

        if 'device_id' in message:
            message['device_id'] = str(message['device_id'])

        await self.send(text_data = json.dumps ({
            'message' : message
        }))

class SMReadingsAlert(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("sm_alerts", self.channel_name)
        await self.accept()
    
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard("sm_alerts", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            "sm_alerts",
            {
                'type' : 'sm_alerts_message',
                'message' : message
            }
        )
    
    async def sm_alerts_message(self,event):
        message = event['message']

        if 'device_id' in message:
            message['device_id'] = str(message['device_id'])

        await self.send(text_data=json.dumps({
            'message' : message
        }))
        


class SKReadingsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("sink_readings",self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("sink_readings",self.channel_name)

    async def recieve(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await self.channel_layer.group_send(
            "sink_readings",
            {
                'type' : 'sink_reading_messages',
                'message' : message
            }
        )
    
    async def sink_reading_messages(self,event):
        message = event['message']

        if 'device_id' in message:
            message['device_id']  = str(message['device_id'])

        await self.send(text_data=json.dumps ({
            'message' : message
        }))



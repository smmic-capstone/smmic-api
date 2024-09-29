import json
from channels.generic.websocket import AsyncWebsocketConsumer
from uuid import UUID

class UUIDEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,UUID):
            return obj.hex
        return json.JSONEncoder.default(self,obj)

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

        if 'Sensor_Node' in message:
            message['Sensor_Node'] = str(message['Sensor_Node'])

        await self.send(text_data = json.dumps ({
            'message' : message
        }))


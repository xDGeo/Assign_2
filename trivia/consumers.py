import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = f'game_{self.game_id}'

        # join game
        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave game group
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # send and receive socket messages
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'game_message',
                'message': message
            }
        )

    async def game_message(self, event):
        message = event['message']

        #receive message from game group through websocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

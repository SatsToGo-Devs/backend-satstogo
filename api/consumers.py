import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger(__name__)

class WebSocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        k1 = self.scope['url_route']['kwargs']['k1']
        self.room_name = f"user_{k1}"
        self.room_group_name = f"user_group_{k1}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            await self.send(text_data=json.dumps({
                    'message': message
                }))
        except Exception as e:
            logger.critical(f"Err-WS-receive:: {e}")

    async def auth_verification(self, data):
        try:
            await self.send(json.dumps(data))
        except Exception as e:
            logger.critical(f"Err-WS-auth_verification:: {e}")

    async def send_message(room_group_name, message):
        try:
            channel_layer = get_channel_layer()
            await channel_layer.group_send(room_group_name, message)
            logger.critical(f"Message sent to group: {room_group_name}")
        except Exception as e:
            logger.critical(f"Error sending message to group {room_group_name}: {e}")


class PaymentUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'invoice_updates'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_invoice_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
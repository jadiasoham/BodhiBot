import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .tasks import generate_response_task
from .services.chat_service import create_message, start_a_chat
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Enter a group"""
        print("starting ws connection")
        self.user = self.scope["user"]

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Check if authenticated:
        if not self.user.is_authenticated:
            await self.close()
            return

        # Join the room/ group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        # Create a Chat object
        self.chat = await sync_to_async(start_a_chat)(username=self.user.username, chat_name=self.room_name)


        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected to BodhiBot"}))

    async def disconnect(self, code):
        """Exit the group"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("content", "")
        context = data.get("context", "")
        summary = data.get("summary", "")

        # Create a message object:
        await sync_to_async(create_message)(chat=self.chat, sender=self.user.username, content=message)

        # Celery task to generate the response
        task = generate_response_task.delay(message, context, summary)

        response = task.get(timeout= 90) # Wait atleast 90 seconds before breaking the pipe.

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": response
            }
        )

        # Record the response as a message object as well:
        await sync_to_async(create_message)(chat= self.chat, sender= "BodhiBot", content= response)

    async def chat_message(self, event):
        await self.send(text_data= json.dumps({
            "message": event["message"]
        }))

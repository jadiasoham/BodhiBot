import json
from datetime import datetime
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from .tasks import generate_response_task
from .services.chat_service import create_message, start_a_chat, get_n_messages_in_chat
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from .models import Chat, Message
from collections import deque
from django.conf import settings
from urllib.parse import quote

User = get_user_model()

async def authenticate_token(token):
    try:
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        user = await sync_to_async(User.objects.get)(id=user_id)
        print(user.username)
        print(user)
        return user
    except Exception:
        raise Exception("User Unauthenticated!")

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Enter a group"""
        try:
            token = self.scope["query_string"].decode().split("=")[-1]
            self.user = await authenticate_token(token)

            self.room_name = self.scope['url_route']['kwargs']['room_name']
            print("This is the chat_title: ", quote(self.room_name), " which is actually: ", self.room_name)
            self.room_group_name = f"chat_{quote(self.room_name)}"
            self.history = deque(maxlen= settings.CHAT_HISTORY_LEN)
            # Initially each element of self.history will contain all the fields returned by the message's serializer.
            # Minimally it should just contain a sender and content field.

            # Join the room/ group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )

            # Check if authenticated, if not immedeatly close connection:
            if not self.user.is_authenticated:
                await self.close()
                return

            # Create a Chat object
            print("start a chat")
            self.chat = await sync_to_async(start_a_chat)(username=self.user.username, chat_name=quote(self.room_name))
            print(str(self.chat))
            message_history = await sync_to_async(get_n_messages_in_chat)(self.chat, settings.CHAT_HISTORY_LEN)
            self.history.extend(message_history)

            await self.accept()
            await self.send(text_data=json.dumps({"message": "Connected to BodhiBot"}))
        except Exception as e:
            print(e)
            self.close()

    async def disconnect(self, code):
        """Exit the group"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")
        # context = data.get("context", "")
        context = self.history
        summary = data.get("summary", "")

        # Create a message object:
        print("got a message for bot!")
        await sync_to_async(create_message)(chat=self.chat, sender=self.user.username, content=message)
        # self.history.append({"sender": self.user.username, "content": message})
        # print(self.history)


        # Celery task to generate the response
        task = generate_response_task.delay(message, list(context), summary)

        self.history.append({"sender": self.user.username, "content": message})

        response = task.get(timeout= 90) # Wait atleast 90 seconds before breaking the pipe.

        bot_message_for_frontend = {
            'id': str(uuid.uuid4()), # Generate a unique ID for React's key prop
            'content': response, # The actual text content
            'sender': 'BodhiBot', # The sender for this message
            'timestamp': datetime.now().isoformat() + 'Z' # Current timestamp
        }

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": bot_message_for_frontend
            }
        )

        # Record the response as a message object as well:
        print("bot has responded - sending to user...")
        await sync_to_async(create_message)(chat= self.chat, sender= "BodhiBot", content= response)
        self.history.append({"sender": "bodhibot", "content": response})

    async def chat_message(self, event):
        await self.send(text_data= json.dumps({
            "type": "chat.message",
            "message": event["message"]
        }))


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # This is crucial for the WebSocket connection to be established
        await self.accept()
        print("WebSocket connected!") # Check your Daphne/console logs for this

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected with code: {close_code}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(f"Received message: {message}")

        await self.send(text_data=json.dumps({
            'message': f'You said: {message}'
        }))
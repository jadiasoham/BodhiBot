from ..models import Chat, Message
from ..serializers import MessageSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
import time
from urllib.parse import unquote

User = get_user_model()


def start_a_chat(username, chat_name):
    """Creates a chat object and returns or retrieves an existing chat."""
    try:
        user = get_object_or_404(User, username= username)
    except Exception as e:
        print(e)
        return
    chat, created = Chat.objects.get_or_create(
        user= user,
        name= unquote(chat_name),
    )

    if created:
        print(f"New chat session {chat_name} started by {user.username} at {time.time()}.")
    else:
        print(f"Existing chat session {chat_name} continued by {user.username} at {time.time()}")

    return chat

def create_message(chat, sender, content):
    """Creates a message object associated to the given chat."""
    
    message_data = {"chat": chat.id, "sender": sender, "content": content}
    serializer = MessageSerializer(data= message_data)
    serializer.is_valid(raise_exception= True)
    serializer.save()
    
    return serializer.data

def get_n_messages_in_chat(chat, n, *, orderby= "-timestamp"):
    """Returns serialized data of n messages, ordered by the requested criterion"""
    messages = Message.objects.filter(chat= chat).order_by(orderby)[:n]
    if orderby.startswith("-"):
        messages = list(reversed(messages))
    
    serializer = MessageSerializer(messages, many= True)
    data = serializer.data
    for msg_data in data:
        for key in list(msg_data):
            if key.lower() not in ["sender", "content"]:
                msg_data.pop(key, None)
    
    return data



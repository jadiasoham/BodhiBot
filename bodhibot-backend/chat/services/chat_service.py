from ..models import Chat
from ..serializers import MessageSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
import time

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
        name= chat_name,
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


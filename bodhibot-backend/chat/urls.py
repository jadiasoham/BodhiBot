from django.urls import path
from .views import UserChatView, MessageView, debug_headers_view

urlpatterns = [
    path('my-chats/', UserChatView.as_view(), name='user-chats'),
    path('messages/', MessageView.as_view(), name= 'chat-messages'),
    path('ws/test/', debug_headers_view, name= 'debug_headers_view')
]
from django.urls import path
from .views import UserChatView

urlpatterns = [
    path('my-chats/', UserChatView.as_view(), name='user-chats'),
]
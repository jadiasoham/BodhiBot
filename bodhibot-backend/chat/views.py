from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .paginators import ChatCursorPagination
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

class UserChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            chats = Chat.objects.filter(user= request.user).order_by('-last_message')
        except Exception as e:
            return Response({"error": e}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not chats.exists():
            return Response({"message": "no chats to load"}, status= status.HTTP_404_NOT_FOUND)
        serializer = ChatSerializer(chats, many= True)
        return Response(serializer.data, status= status.HTTP_202_ACCEPTED)
    
    def post(self, request):
        data = request.data

        chat_data = {
            "user": request.user.id,
            "name": data.get("name", "Unnamed")
        }

        serializer = ChatSerializer(data= chat_data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)   

class MessageView(APIView):
    """This will send over the current message history stored on the users chat to the server on opening the given chat."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = request.query_params

        chats = Chat.objects.filter(user= user, name= data.get("name"))

        if chats.count() > 1:
            return Response({"error": "More than 1 chats found."}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not chats.exists():
            return Response({"error": "No chat records found"}, status= status.HTTP_404_NOT_FOUND)
        
        chat = chats.first()
        messages = Message.objects.filter(chat= chat).order_by('-timestamp')

        paginator = ChatCursorPagination()
        result_page = paginator.paginate_queryset(messages, request)

        serializer = MessageSerializer(messages, many= True)
        return paginator.get_paginated_response(serializer.data)
        
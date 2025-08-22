from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .permissions import PolicyAccessPermissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .paginators import ChatCursorPagination
from .models import Chat, Message, GatekeeperLogs, GatekeeperLogReview, UsagePolicy
from .serializers import ChatSerializer, MessageSerializer, UsagePolicySerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from urllib.parse import unquote

class UserChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            chats = Chat.objects.filter(user=request.user).order_by('-last_message')
            serializer = ChatSerializer(chats, many=True)
            response = {
                "status": "ok",
                "data": serializer.data
            }
            if not serializer.data:
                response["message"] = "No chats to load"
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": "Something went wrong. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        data = request.data
        chat_data = {
            "user": request.user.id,
            "name": data.get("name", "Unnamed")
        }
        try:
            serializer = ChatSerializer(data= chat_data)
            serializer.is_valid(raise_exception= True)
            serializer.save()

            response_data = {
                "status": "ok",
                "data": serializer.data
            }
            return Response(response_data, status= status.HTTP_201_CREATED)
        
        except ValidationError as e:
            # If the serializer raises error, then
            return Response(
                {"status": "error", "message": f"Error validating your data, try again later or report this incident."},
                status= status.HTTP_400_BAD_REQUEST
            ) 

        except Exception as e:
            return Response(
                {"status": "error", "message": "Something went wrong, please try again later."},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MessageView(APIView):
    """This will send over the current message history stored on the users chat to the server on opening the given chat."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = request.query_params

        chats = Chat.objects.filter(user= user, room_name= data.get("name"))

        if chats.count() > 1:
            return Response({"status": "error", "message": "More than 1 chats found."}, status= status.HTTP_409_CONFLICT)
        
        if not chats.exists():
            return Response({"status": "ok", "message": "No chat records found", "data": []}, status= status.HTTP_200_OK)
        
        chat = chats.first()
        messages = Message.objects.filter(chat= chat).order_by('-timestamp')

        paginator = ChatCursorPagination()
        result_page = paginator.paginate_queryset(messages, request)

        serializer = MessageSerializer(result_page, many= True)
        paginated_data = paginator.get_paginated_response(serializer.data).data

        return Response({"status": "ok", "data": paginated_data}, status= status.HTTP_200_OK)


class GatekeeperLogs(APIView):
    """Get function to get the logs... (No post because logs get created automatically and ideally are required to be unmodifiable)"""
    def get(self, request):
        pass
        


class ReviewGatekeeperLogs(APIView):
    def get(self, request):
        pass

class UsagePolicyView(APIView):
    """Update and View the usage poilicy"""
    permission_classes = [IsAuthenticated, PolicyAccessPermissions]

    def get(self, request):
        """Anyone can view policy"""
        try:
            policy = UsagePolicy.objects.filter().order_by("-updated_on").first()
            serializer = UsagePolicySerializer(policy)
            return Response({"policy": serializer.data}, status= status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({"message": "An error occurred"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        data = request.data
        try:
            serializer = UsagePolicySerializer(data= data)
            serializer.is_valid(raise_exception= True)
            serializer.save()
            return Response({"data": serializer.data}, status= status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": e.detail}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": "some error"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt # To test ws upgrade
def debug_headers_view(request):
    """
    A view to echo all request headers.
    """
    headers = {key: value for key, value in request.headers.items()}
    return JsonResponse({
        'method': request.method,
        'path': request.path,
        'headers': headers,
        'get_params': request.GET,
        'body': request.body.decode('utf-8', errors='ignore') # Decode body if present
    })

        
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.id, "username": user.username})
    else:
        return Response({"error": "Invalid Credentials"}, status= status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({"message": "Logged out successfully"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_info(request):
    serializer = UserSerializer(request.user)
    return Response({"status": "ok", "data": serializer.data}, status=status.HTTP_200_OK)
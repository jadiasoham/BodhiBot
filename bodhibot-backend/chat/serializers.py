from .models import Chat, Message, GatekeeperLogs, GatekeeperLogReview
from rest_framework.serializers import ModelSerializer

class ChatSerializer(ModelSerializer):
    
    class Meta:
        model = Chat
        fields = '__all__'


class MessageSerializer(ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class GatekeeperLogsSerializer(ModelSerializer):

    class Meta:
        model = GatekeeperLogs
        fields = '__all__'


class GatekeeperLogReview(ModelSerializer):

    class Meta:
        model = GatekeeperLogReview
        fields = '__all__'

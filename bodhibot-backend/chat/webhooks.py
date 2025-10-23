from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from os import getenv
from rest_framework.response import Response

class ChatMessageResponseWebhook(APIView):
    """This class defines a POST endpoint to return the inferencing response from llm to the correct client's websocket."""

    @csrf_exempt
    def post(self, request):
        data = request.data.copy()

        # Read the secret code to make sure reuqest is from a trustable source.
        # secret = data.get('secret', '')
        # if secret != getenv('WEBHOOK_SECRET'):
        #     print("Unauthenticated request detected on webhook...")
        #     return
        
        # get the channel layer and invoke the group_send method to send message
        channel_layer = get_channel_layer()

        group_name = data.get('group_name', '')
        message_type = data.get('message_type', 'chat_message')
        content = data.get('content', '')

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": message_type,
                "message": content
            }
        )
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "update_history",
                "value": {"sender": "bodhibot", "content": content['content']}
            }
        )

        return Response({'status': 'ok'})

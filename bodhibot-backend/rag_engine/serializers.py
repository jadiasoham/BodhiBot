from .models import Document
from rest_framework.serializers import ModelSerializer

class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at']

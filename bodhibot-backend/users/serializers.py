from .models import User
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_org_admin",
            "is_superuser",
        ]

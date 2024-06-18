from .models import SatsUser
from rest_framework import serializers

class SatsUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = SatsUser
    fields = ['magic_string', 'first_name', 'last_name','created_at', 'last_login']

class TokenSerializer(serializers.Serializer):
  email = serializers.EmailField(required=False)
  password = serializers.CharField(required=False)
  magic_string = serializers.CharField(required=False)

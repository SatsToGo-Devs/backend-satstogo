from sattogo.middleware import BaseSerializer
import pytz
from .models import SatsUser
from rest_framework import serializers,validators

class SatsUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = SatsUser
    fields = ['magic_string', 'first_name', 'last_name','created_at', 'last_login']
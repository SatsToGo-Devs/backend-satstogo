from rest_framework import serializers
from organizer.models import Events, Organizer


class OrganizerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organizer
        fields = ['name','is_businesss']
    


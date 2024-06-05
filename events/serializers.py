from sattogo.middleware import BaseSerializer
import pytz
from .models import Event, EventSession, Attendance
from api.models import SatsUser
from rest_framework import serializers,validators

class EventSessionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSession
        fields = ['pk','title', 'deadline']  # Specify desired fields


class ConfirmEventSerialiazer(serializers.Serializer):
    pk = serializers.CharField(max_length=100)
    magic_string = serializers.CharField(max_length=300)


    def missing_fields(self, data):
        """
            Custom validation to ensure both 'pk' and 'magic_string' are present.

            Raises a ValidationError if either field is missing.
        """
        
        required_fields = ['pk', 'magic_string']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            raise serializers.ValidationError({
                'error': f"Missing required fields: {', '.join(missing_fields)}"
            })

    def user_is_allowed(self,data):
        magic_string = data.get('magic_string')
        pk = data.get('pk')
        matching_event_session = EventSession.get_method(pk=pk)
        parent_event = matching_event_session.parent_event

        if parent_event.access != 'public':
            guest  =  matching_event_session.attendance_set.all().filter(user__magic_string=magic_string)
            # print('attendance',attendance)
            if not guest:
                raise serializers.ValidationError(detail='You are not on the list for this event',code=401)
        
    def validate(self, data):
        self.missing_fields(data)

        # self.user_is_allowed(data)
        return data
        
    class Meta:
        model = EventSession
        fields = ['pk','magic_string']  # Specify desired fields


class AttendanceSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    # ... other fields
    def is_unique(self,data):
        magic_string = data.get('user')
        event = data.get('event')
        existing_match = Attendance.objects.filter(user__magic_string=magic_string, event=event).first()
        
        if existing_match:            
            raise serializers.ValidationError({
                'error': f"You have already registered for this event"
            })

    def validate(self, data):
        self.is_unique(data)
        return data

    class Meta:
        model = Attendance
        fields = ['first_name','last_name','user','event']
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Attendance.objects.all(),
                fields=["user", "event"],
                message=('This user has already registered for this')
            )
        ]

    def create(self, validated_data):
        user = validated_data.pop('user')
        new_user = SatsUser.objects.get(magic_string=user)
        print('new user',validated_data)
        new_attendance = Attendance.objects.create(user=new_user, **validated_data)
        return new_attendance


class EventReadSerializer(serializers.ModelSerializer):
    sessions = EventSessionReadSerializer(source='eventsession_set', many=True)
    class Meta:
        model = Event
        fields = ('name', 'event_type', 'venue', 'reward','timezone','access', 'sessions')


class EventSerializer(serializers.ModelSerializer):
    new_created_at = serializers.SerializerMethodField()
    event_deadline = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = '__all__'
        validators = [
            BaseSerializer.validate_required
        ]
        extra_fields = ['new_created_at', 'event_deadline']

    def get_new_created_at(self, obj):
        timezone_selected = pytz.timezone(obj.timezone)
        created_at_local = obj.created_at.astimezone(timezone_selected)
        return created_at_local.strftime('%m/%d/%Y %H:%M')

    def get_event_deadline(self, obj):
        timezone_selected = pytz.timezone(obj.timezone)
        deadline_local = obj.deadline.astimezone(timezone_selected)
        return deadline_local.strftime('%m/%d/%Y %H:%M')

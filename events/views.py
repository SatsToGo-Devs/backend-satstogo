from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.decorators import api_view
from datetime import datetime
from .models import Event, Attendance,EventSession
from api.models import SatsUser, User
from .serializers import EventSerializer, EventReadSerializer, ConfirmEventSerialiazer

class EventCrud(APIView):
    serializer_class = EventSerializer

    def create(self, request):
        # Override create to handle attendee data (assuming data format)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message":"Event created successfully!",
            "data": serializer.data
        })

    def get(self,request):
        events = Event.objects.prefetch_related('eventsession_set')
        print('events',events)
        serializer = EventReadSerializer(events, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        # events = Event.objects.prefetch_related('eventsession_set')
        # my_events = []

        # for event in events:
        #     # Create a dictionary for each event
        #     sessions = event.eventsession_set.all()
        #     event_dict = {
        #         'name': event.name,
        #         'deadline': str(event.deadline),
        #         'event_type': event.event_type,
        #         'venue': event.venue,
        #         'reward': event.reward,
        #         'sessions': sessions # List to hold session data
        #     }
        #     my_events.append(event_dict)
        # return Response({
        #     "message":"Event created successfully!",
        #     "data": json.dumps(my_events)
        # },status=status.HTTP_200_OK)

# request a new confirmation email
class ActivateUser(APIView):
    serializer_class = ConfirmEventSerialiazer

    def post(self, request):
        serialize_data = self.serializer_class(data=request.data)
        if serialize_data.is_valid():
            try:
                pk = request.data.get('pk')
                magic_string = request.data.get('magic_string')
                matching_user = SatsUser.objects.get(magic_string=magic_string)
                session = EventSession.objects.prefetch_related('parent_event').get(pk=pk)
                parent_event = session.parent_event
                formatted_datetime = datetime.now().time()
                deadline_to_time = session.deadline.time()
                print('comparing time',formatted_datetime, deadline_to_time)
                if formatted_datetime < deadline_to_time:
                    status = 200
                    responsedict = {'message': f'Congrats!! you have won ${parent_event.reward} Sats.'}
                    is_activated = True
                else:
                    responsedict = {'error': 'Oops, you are not eligible to receive this reward'}
                    status = 403
                    is_activated = False
                Attendance(user=matching_user,event=session,is_activated=is_activated).save()
                print(responsedict)
            except (SatsUser.DoesNotExist, EventSession.DoesNotExist):
                responsedict = {'error': 'User or Event does not exist'}
                status = 404
        else:
            responsedict = serialize_data.errors
            status = 400

        return Response(responsedict,status=status)









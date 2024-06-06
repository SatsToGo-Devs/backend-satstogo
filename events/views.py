import requests
from django.conf import settings
import pytz
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from .models import Event, Attendance,EventSession
from api.models import SatsUser
from .serializers import EventSerializer, EventReadSerializer, ConfirmEventSerialiazer, AttendanceSerializer


ADMIN_API_KEY = settings.ADMIN_API_KEY
LNURL_ENDPOINT = settings.LNURL_ENDPOINT
INVOICE_READ_KEY = settings.INVOICE_READ_KEY
LNURL_PAYMENTS_ENDPOINT = settings.LNURL_PAYMENTS_ENDPOINT

class EventCrud(APIView):
    serializer_class = EventSerializer
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Event created successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def create(self, request):
        # Override create to handle attendee data (assuming data format)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={
            "message":"Event created successfully!",
            "data": serializer.data
        })

    def get(self,request):
        events = Event.objects.prefetch_related('eventsession_set')
        print('events',events)
        serializer = EventReadSerializer(events, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
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

class ActivateUser(APIView):

    serializer_class = ConfirmEventSerialiazer

    def post(self, request):
        serialize_data = self.serializer_class(data=request.data)
        if serialize_data.is_valid():
            try:
                pk = request.data.get('pk')
                magic_string = request.data.get('magic_string')
                user = SatsUser.objects.get(magic_string=magic_string)
                session = EventSession.objects.prefetch_related('parent_event').get(pk=pk)
                parent_event = session.parent_event
                try:
                    alreadyActivated = Attendance.objects.get(user=user,event=parent_event,locked=True)
                    responsedict = {'error': 'You have already activated for this event'}
                    status = 403
                    return Response(data=responsedict,status=status)
                except Attendance.DoesNotExist:
                    print(f"datetime.now(): {datetime.now().time()}")
                    formatted_datetime = datetime.now().time()
                    print(f"formatted_datetime: {formatted_datetime}")
                    deadline_to_time = session.deadline.time()
                    print(f"deadline_to_time: {deadline_to_time}")
                    if formatted_datetime < deadline_to_time:
                        user.update_sats_balance(user.sats_balance+parent_event.reward)
                        status = 200
                        responsedict = {'message': f'Congrats!! you have won ${parent_event.reward} Sats.'}
                        is_activated = True
                    else:
                        responsedict = {'error': 'Oops, you are not eligible to receive this reward'}
                        status = 403
                        is_activated = False
                    new_attendance = Attendance.objects.update_or_create(
                        user=user,
                        event=parent_event,
                        defaults={
                            "event": parent_event,
                            "eventSession": session,
                            "is_activated":is_activated,
                            "locked": True,
                            "clock_in_time":datetime.today()
                        }
                    )
            except (SatsUser.DoesNotExist, EventSession.DoesNotExist):
                responsedict = {'error': 'User or Event does not exist'}
                status = 404
        else:
            responsedict = serialize_data.errors
            status = 400

        return Response(data=responsedict,status=status)

class RegisterUser(APIView):
    serializer_class = AttendanceSerializer

    def post(self, request):
        # Override create to handle attendee data (assuming data format)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={
                "message":"User has registered for event successfully!",
                "data": serializer.data
            },
            status=201
        )

    def get(self,request):
        try:
            event_id = request.query_params.get('event_id')
            event = Event.get_method(pk=event_id)
            responsedict = event
            status = 200
        except(Event.DoesNotExist): 
            responsedict = {'error': 'Event does not exist'}
            status = 404
        except Exception:
            responsedict = {'error': 'An unexpected error occured'}
            status = 500
        return Response(data=responsedict,status=status)

class RewardView(APIView):
    def generate_lnurl(self, request):
        title = request.GET.get("title")
        min_withdrawable = request.GET.get("min_withdrawable")
        max_withdrawable = request.GET.get("max_withdrawable")
        uses = request.GET.get("uses")
        wait_time = request.GET.get("wait_time")
        is_unique = request.GET.get("is_unique")
        webhook_url = request.GET.get("webhook_url")
        admin_key = request.GET.get("X-Api-Key")
        
        payload = {
            "title": title,
            "min_withdrawable": int(min_withdrawable),
            "max_withdrawable": int(max_withdrawable),
            "is_unique": True,
            "uses": 1, 
            "wait_time": 1
        }

        lnurl_endpoint = LNURL_ENDPOINT

        headers = {"Content-type": "application/json", "X-Api-Key": ADMIN_API_KEY}

        # Making a POST request to the LNURL generation endpoint
        response = requests.post(lnurl_endpoint, json=payload, headers=headers)

        if response.status_code == status.HTTP_201_CREATED:
            lnurl = response.json()
            return Response(data={"lnurl": lnurl}, status=status.HTTP_200_OK)
        else:
            return Response(data={"error": "Failed to generate LNURL"}, status=response.status_code)

    def get(self, request):
        # Call the generate_lnurl method
        return self.generate_lnurl(request)

class WithdrawCallbackView(APIView):
    def get(self, request):
        # Extract k1 token and Lightning invoice from query parameters
        k1_token = request.GET.get('k1')
        invoice = request.GET.get('invoice')
        # create_invoice = {
        #         "unit": "sat",
        #         "internal": False,
        #         "out": False,
        #         "amount": 10,
        #         "memo": "Payment memo", 
        # }
        # headers = {"Content-type": "application/json", "X-Api-Key": INVOICE_READ_KEY}
        # response = requests.post(LNURL_PAYMENTS_ENDPOINT, json=create_invoice, headers=headers)
        # Assuming response.content contains the JSON data
        # response_data = json.loads(response.content.decode('utf-8'))
        # payment_request = response_data.get("payment_request")
        pay_invoice = {
            "out": True,
            "bolt11": invoice,
        }
        payment_headers = {"Content-type": "application/json", "X-Api-Key": ADMIN_API_KEY}
        payment_response = requests.post(LNURL_PAYMENTS_ENDPOINT, json=pay_invoice, headers=payment_headers)
        return Response(payment_response.json())







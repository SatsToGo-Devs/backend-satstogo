import requests
import json
from api.models import FcmToken
import firebase_admin
from firebase_admin import credentials, messaging
from asgiref.sync import sync_to_async

class Utils:
    cred = credentials.Certificate("api/utils/service_account.json")
    firebase_admin.initialize_app(cred)
    def send_notification(tokens, notification, dry_run=False):
        try:
            message = messaging.MulticastMessage(
            data=notification,
            tokens=tokens,
            )
            response = messaging.send_multicast(message)
            print('{0} FCM notifications were sent successfully'.format(response.success_count))
        except Exception as e:
            print(f"An error occurred while sending FCM: {e}")

    async def notifyUserViaFcm(magic_str,notif):
        try:
            print(f"magic_str: {magic_str}")
            fcmToken = await sync_to_async(FcmToken.objects.get)(magic_string=magic_str)
            print(f"FCM: {fcmToken}")
            Utils.send_notification([fcmToken.token],notif)
        except Exception as e:
            print(f"An error occurred while sending FCM: {e}")
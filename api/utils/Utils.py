import requests
import json
import firebase_admin
from firebase_admin import credentials, messaging

class Utils:
    cred = credentials.Certificate("api/utils/service_account.json")
    firebase_admin.initialize_app(cred)
    def send_notification(tokens, notification, dry_run=False):
        message = messaging.MulticastMessage(
        data=notification,
        tokens=tokens,
        )
        response = messaging.send_multicast(message)
        print('{0} FCM notifications were sent successfully'.format(response.success_count))
import json
import os
from django.http import JsonResponse
from binascii import unhexlify
from api.utils.Utils import Utils
from secp256k1 import PublicKey
from .models import FcmToken, SatsUser,SatsUser, SatsUserProfile
import os
import random
import string
import lnurl
import random
import api.consumers as consumers
from rest_framework.views import APIView
from django.conf import settings
from asgiref.sync import sync_to_async
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

ADMIN_API_KEY = settings.ADMIN_API_KEY
LNURL_ENDPOINT = settings.LNURL_ENDPOINT
INVOICE_READ_KEY = settings.INVOICE_READ_KEY
LNURL_PAYMENTS_ENDPOINT = settings.LNURL_PAYMENTS_ENDPOINT

class AuthView(APIView):
    @csrf_exempt
    def auth_login_view(request):
        try:
            magic_str = request.GET.get('k1')
            user = SatsUser.objects.get(magic_string=magic_str)
            pubkey = PublicKey(unhexlify(user.key), raw=True)
            sig_raw = pubkey.ecdsa_deserialize(unhexlify(user.sig))
            r = pubkey.ecdsa_verify(unhexlify(magic_str), sig_raw, raw=True)
            if(r == True):
                user.update_last_login()
                print(user)
                return JsonResponse({"status": "OK"})
            else:
                return JsonResponse({"status": "ERROR", "message": "Unable to Verify Magic String"})
        except SatsUser.DoesNotExist:
            print("SatsUser not found with magic string:", magic_str)
            return JsonResponse({"status": "ERROR", "message": "Magic String Not Found"})
        except SatsUser.MultipleObjectsReturned:
            print("Multiple users found with magic string:", magic_str)
            return JsonResponse({"status": "ERROR", "message": "Multiple Magic String Found"})

    @csrf_exempt
    def auth_view(request):
        random_data = os.urandom(32)
        hex_data = '00' + random_data.hex()[2:64]

        try:
            data = json.loads(request.body)
            firebase_token = data.get('firebase_token')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            tk = FcmToken.objects.update_or_create(magic_string=hex_data, token=firebase_token,defaults={'magic_string': hex_data,'token':firebase_token},)
            p = SatsUserProfile.objects.update_or_create(magic_string=hex_data,defaults={'first_name': first_name,'last_name':last_name},)
            print(tk)
            print(p)
        except IntegrityError as e:
            print(e)
        
        if request.is_secure():
            base_uri = request.build_absolute_uri('/')
        else:
            base_uri = request.build_absolute_uri('/').replace('http:', 'https:')

        auth_url = f"{base_uri}api/auth-verify/?tag=login&k1={hex_data}&action=login"        
        response = {
            "status": "OK",
            "magic_string": hex_data,
            "auth_url": auth_url,
            "encoded": lnurl.encode(auth_url)
        }

        return JsonResponse(response)

    async def auth_verify_view(request):
        k1 = request.GET.get('k1')
        key = request.GET.get('key')
        sig = request.GET.get('sig')

        pubkey = PublicKey(unhexlify(key), raw=True)
        sig_raw = pubkey.ecdsa_deserialize(unhexlify(sig))
        r = pubkey.ecdsa_verify(unhexlify(k1), sig_raw, raw=True)
        if(r == True):
            try:
                user=SatsUser(magic_string=k1,key=key,sig=sig)
                await sync_to_async(user.save)()
            except IntegrityError as e:
                print(e)
                
            await consumers.WebSocketConsumer.send_message(f"user_group_{k1}",{"type": "auth_verification","status": "OK","message":"Verification Successful"})
            await Utils.notifyUserViaFcm(k1)
            return JsonResponse({"status": "OK"})
        else:
            return JsonResponse({"status": "ERROR", "message": "Unable to verify"})

    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))


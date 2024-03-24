from django.shortcuts import render
from django.http import JsonResponse
from binascii import unhexlify
from secp256k1 import PublicKey
from .models import User
from django.utils import timezone
import os
import random
import string
import asyncio
import datetime
import random
import segno
import websockets


def auth_login_view(request):
    try:
        magic_str = request.GET.get('magic_string')
        user = User.objects.get(magic_string=magic_str)
        pubkey = PublicKey(unhexlify(user.key), raw=True)
        sig_raw = pubkey.ecdsa_deserialize(unhexlify(user.sig))
        r = pubkey.ecdsa_verify(unhexlify(magic_str), sig_raw, raw=True)
        if(r == True):
            user.update_last_login()
            print(user)
            return JsonResponse({"status": "OK"})
        else:
            return JsonResponse({"status": "ERROR", "reason": "Unable to Verify Magic String"})
    except User.DoesNotExist:
        print("User not found with magic string:", magic_str)
        return JsonResponse({"status": "ERROR", "reason": "Magic String Not Found"})
    except User.MultipleObjectsReturned:
        print("Multiple users found with magic string:", magic_str)
        return JsonResponse({"status": "ERROR", "reason": "Multiple Magic String Found"})



def auth_view(request):
    random_data = os.urandom(32)
    hex_data = '00' + random_data.hex()[2:64]
    qrcode = segno.make_qr(f"https://moose-fair-publicly.ngrok-free.app/api/auth-verify/?tag=login&k1={hex_data}&action=login").svg_data_uri(scale=10)
    return JsonResponse({"status": "OK","qrcode":qrcode,"magic_string":hex_data})

def auth_verify_view(request):
    k1 = request.GET.get('k1')
    key = request.GET.get('key')
    sig = request.GET.get('sig')

    pubkey = PublicKey(unhexlify(key), raw=True)
    sig_raw = pubkey.ecdsa_deserialize(unhexlify(sig))
    r = pubkey.ecdsa_verify(unhexlify(k1), sig_raw, raw=True)
    if(r == True):
        user=User(magic_string=k1,key=key,sig=sig)
        user.save()
        print(user)
        return JsonResponse({"status": "OK"})
    else:
        return JsonResponse({"status": "ERROR", "reason": "Unable to verify"})



def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))
from django.shortcuts import render
from django.http import JsonResponse
import segno
from binascii import unhexlify
from secp256k1 import PublicKey
import os
import random
import string

def login_view(request):
    # Retrieve data from the database or any other source
    k1 = unhexlify(request.GET.get('k1'))
    key = unhexlify(request.GET.get('key'))
    sig = unhexlify(request.GET.get('sig'))

    pubkey = PublicKey(key, raw=True)
    sig_raw = pubkey.ecdsa_deserialize(sig)
    r = pubkey.ecdsa_verify(k1, sig_raw, raw=True)
    print(r)
    if(r == True):
        return JsonResponse({"status": "OK"})
    else:
        return JsonResponse({"status": "ERROR", "reason": "Unable to verify"})

def get_magic_string(request):
    random_data = os.urandom(32)
    hex_data = '00' + random_data.hex()[2:64]
    path=f"{generate_random_string(4)}.png"

    qrcode = segno.make_qr(f"https://moose-fair-publicly.ngrok-free.app/api/login/?tag=login&k1={hex_data}&action=login")
    qrcode.save(
        f"media/{path}",
        scale=5,
        dark="darkblue",
    )
    return JsonResponse({"status": "OK","qrcode":f"https://moose-fair-publicly.ngrok-free.app/{path}"})

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))
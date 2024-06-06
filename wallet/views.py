import json
import os
from django.http import JsonResponse
from binascii import unhexlify
from api.utils.Utils import Utils
from secp256k1 import PublicKey
import os
import random
import string
import lnurl
import random
import requests
from datetime import datetime, timedelta
import time
import api.consumers as consumers
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from asgiref.sync import sync_to_async
from api.models import SatsUser
from wallet.models import WithdrawalRequest

ADMIN_API_KEY = settings.ADMIN_API_KEY
LNURL_ENDPOINT = settings.LNURL_ENDPOINT
INVOICE_READ_KEY = settings.INVOICE_READ_KEY
LNURL_PAYMENTS_ENDPOINT = settings.LNURL_PAYMENTS_ENDPOINT
BLINK_API_KEY = settings.BLINK_API_KEY
BLINK_API_URL = settings.BLINK_API_URL
BLINK_SATS_WALLET_ID=settings.BLINK_SATS_WALLET_ID

class WalletEndpoints(APIView):
    def account(request):
        blink_wallet = BlinkWallet()
        info = blink_wallet.wallet_info()
        if info is None:
            return JsonResponse("Unable to get Wallet data")
        else:
            print("Info: ${info}")
            return JsonResponse(info)
        
    def receive(request):
        blink_wallet = BlinkWallet()
        info = blink_wallet.receive()
        if info is None:
            return JsonResponse("Unable to get receive invoice")
        else:
            print("Info: ${info}")
            return JsonResponse(info)
        
    def estimate_payment_fee(request):
        blink_wallet = BlinkWallet()
        fee = blink_wallet.estimate_payment_fee()
        if fee is None:
            return JsonResponse("Unable to estimate payment fee")
        else:
            print("Info: ${info}")
            return JsonResponse(fee)


class BlinkWallet():
    wallet_id=BLINK_SATS_WALLET_ID
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": BLINK_API_KEY,
        }
    def wallet_info(self):
        try:
            query = """
                query me {
                me {
                    defaultAccount {
                    wallets {
                        id
                        walletCurrency
                        balance
                    }
                    }
                }
                }
                """
            data = {"query": query, "variables": {}}
            response = requests.post(BLINK_API_URL, headers=self.headers, json=data)

            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Error: {response.status_code}")
            
                return JsonResponse({"status": "OK"})
        except Exception as e:
            print("SatsUser not found with magic string:", e)
        return None

    def receive(self):
        query = """
            mutation LnInvoiceCreate($input: LnInvoiceCreateInput!) {
            lnInvoiceCreate(input: $input) {
                invoice {
                paymentRequest
                paymentHash
                paymentSecret
                satoshis
                }
                errors {
                message
                }
            }
            }
         """
        input_data = {"amount": "18", "walletId": self.wallet_id}
        data = {"query": query, "variables": {"input": input_data}}

        response = requests.post(BLINK_API_URL, headers=self.headers, json=data)
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print(f"Error creating invoice: {data['errors'][0]['message']}")
            else:
                invoice = data["data"]["lnInvoiceCreate"]["invoice"]
                print(f"Invoice created successfully:")
                print(f"\tPayment Request: {invoice['paymentRequest']}")
                print(f"\tPayment Hash: {invoice['paymentHash']}")
                print(f"\tPayment Secret: {invoice['paymentSecret']}")
                print(f"\tSatoshis: {invoice['satoshis']}")
            return data
        else:
            print(f"Error: {response.status_code}")
            return None
        
    def estimate_payment_fee(self):
        query = """
        mutation lnInvoiceFeeProbe($input: LnInvoiceFeeProbeInput!) {
        lnInvoiceFeeProbe(input: $input) {
            errors {
            message
            }
            amount
        }
        }
        """
        payment_request = "lnbc180n1pn97q2cpp54vkyz80s242r84j6znjznx0wwtgwezznr3nqwsenjrvdwr6twwnqdqqcqzpuxqyz5vqsp5ygnpjytaq20qf6nhd3phhr9pv7ajum9fspk4ftccdz3pwjzjn8xs9qyyssqy388a3yaf4zp5qut5chaapl7twacprrmaf9n8zenepnznm38ugche9ed6vcx7r7ypfnap8ggejem3597282pt58khvqz83zc77w7tyspgk450c"
        input_data = {"paymentRequest": payment_request, "walletId": self.wallet_id}
        data = {"query": query, "variables": {"input": input_data}}
        response = requests.post(BLINK_API_URL, headers=self.headers, json=data)
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print(f"Error estimating fee: {data['errors'][0]['message']}")
                return None
            else:
                estimated_fee = data["data"]["lnInvoiceFeeProbe"]["amount"]
                print(f"Estimated fee for invoice: {estimated_fee} Satoshis")
                return data
        else:
            print(f"Error: {response.status_code}")
        return None
    
    def ln_invoice_payment_send(self,payment_request):
        query = """
        mutation LnInvoicePaymentSend($input: LnInvoicePaymentInput!) {
            lnInvoicePaymentSend(input: $input) {
            status
            errors {
                message
                path
                code
            }
            }
        }
        """

        variables = {
            "input": {
                "paymentRequest": payment_request,
                "walletId": self.wallet_id,
            }
        }
        response = requests.post(BLINK_API_URL, headers=self.headers, json={'query': query, 'variables': variables})

        if response.status_code == 200:
            data = response.json()['data']['lnInvoicePaymentSend']
            print(f"{data}")

            if "errors" in data and data["errors"]:
                print(f"Error paying: {data['errors'][0]['message']}")
                return None
            else:
                status = data["status"]
                print(f"Blink Invoice Payment: {status}")
                return status
        else:
            print(f"Error: {response.status_code}")
            return None
        

class LnurlWithdrawal(APIView):
    def get_base_url(request):
        if request.is_secure():
            return request.build_absolute_uri('/')
        else:
            return request.build_absolute_uri('/').replace('http:', 'https:')
    def generate_lnurl_withdraw_callback(base_url,magic_string):
        five_minutes_from_now = datetime.now()+ timedelta(minutes=5) 
        expiry = int(five_minutes_from_now.timestamp())
        withdraw_url = f"{base_url}wallet/initiate-withdrawal/?expiry={expiry}&magic_string={magic_string}"
        print(f"withdraw_url: {withdraw_url}")
        return lnurl.encode(withdraw_url)
    
    @csrf_exempt
    def get_lnurl_withdraw_link(request):
        try:
            magic_string = request.GET.get('magic_string')
            base_uri=LnurlWithdrawal.get_base_url(request=request)
            link=LnurlWithdrawal.generate_lnurl_withdraw_callback(base_uri,magic_string)
            print(f"get_lnurl_withdraw_link: {link}")
            return JsonResponse({
            "status": "OK",
            "data": {'link':link},
            })
        except Exception as e:
            print(e)
            return JsonResponse({
            "status": "ERROR",
            "message": 'Request Failed',
            })
        

    def initiate_withdrawal(request):
        expiry = request.GET.get('expiry')
        magic_string = request.GET.get('magic_string')
        user = SatsUser.objects.get(magic_string=magic_string)
        try:
            now_epoch = int(datetime.now().timestamp())
            if now_epoch > int(expiry):
                raise Exception('Payment Request Expired')

            base_uri=LnurlWithdrawal.get_base_url(request=request)
            min_withdrawable=2
            max_withdrawable=10
            w_req = WithdrawalRequest(expiry=expiry,user=user,max_withdrawable=max_withdrawable, min_withdrawable=min_withdrawable)
            w_req.save()

            payload = {
            "tag": "withdrawRequest",
            "callback": f"{base_uri}wallet/confirm-withdrawal/",
            "k1": w_req.pk,
            "defaultDescription": 'SatsToGO! accumulated sats withdrawal',
            "minWithdrawable":min_withdrawable,
            "maxWithdrawable":max_withdrawable
            }

            return JsonResponse(payload)
        except Exception as e:
            print(e)
            return JsonResponse({"status": "ERROR", "reason": "Unable to Initiate Payment Request"})
        
    def confirm_withdrawal(request):
        k1 = request.GET.get('k1')
        pr = request.GET.get('pr')
        try:
            w_req = WithdrawalRequest.objects.get(pk=k1)
            now_epoch = int(datetime.now().timestamp())
            if now_epoch > w_req.expiry:
                raise Exception('Payment Request Expired')
            
            blink_wallet=BlinkWallet()
            status=blink_wallet.ln_invoice_payment_send(payment_request=pr)

            if status is None:
                raise Exception('Unable to complete payment request')
            else:
                w_req.funds_claimed=True
                w_req.save()
                return JsonResponse({"status": "OK"})
            
        except Exception as e:
            print(e)
            return JsonResponse({"status": "ERROR", "reason": "Unable to complete payment request"})
                


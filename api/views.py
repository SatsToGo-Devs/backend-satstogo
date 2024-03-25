import lightning_pb2 as ln
import lightning_pb2_grpc as lnrpc
import grpc
import os
import requests
import codecs
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework import status
from lnurl import Lnurl
import utils


class RewardView(APIView):
    def generate_lnurl(self, request):
        # Assuming you extract necessary parameters from the request
        title = request.GET.get("title")
        min_withdrawable = request.GET.get("min_withdrawable")
        max_withdrawable = request.GET.get("max_withdrawable")
        uses = request.GET.get("uses")
        wait_time = request.GET.get("wait_time")
        is_unique = request.GET.get("is_unique")
        webhook_url = request.GET.get("webhook_url")
        admin_key = request.GET.get("X-Api-Key")

        # Assuming you construct the JSON payload
        payload = {
            "title": "Test1",
            "min_withdrawable": 10,
            "max_withdrawable": 20,
            "is_unique": True,
            "uses": 1, 
            "wait_time": 1
        }

        # import pdb; pdb.set_trace()
        lnurl_endpoint = "https://legend.lnbits.com/withdraw/api/v1/links"

        headers = {"Content-type": "application/json", "X-Api-Key": "1a9ca9d92e5d4c66837fd77049a235fc"}

        # Making a POST request to the LNURL generation endpoint
        response = requests.post(lnurl_endpoint, json=payload, headers=headers)

        if response.status_code == status.HTTP_201_CREATED:
            lnurl = response.json()
            return Response({"lnurl": lnurl}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to generate LNURL"}, status=response.status_code)

    def get(self, request):
        # Call the generate_lnurl method
        return self.generate_lnurl(request)
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework import status

class RewardView(APIView):
    def post(self, request):
     # Extract lightning_address and amount from request data
        import pdb; pdb.set_trace()
        lightning_address = request.data.get('lightning_address')
        amount = request.data.get('amount')
        # Check if both fields are provided
        if not (lightning_address and amount):
            return Response({'error': 'Both lightning_address and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)
        import pdb; pdb.set_trace()
        # Connect to Voltage Lightning Node
        try:
            lnd = LNDClient(
                "your_node_address:port",
                macaroon_filepath="/path/to/your/admin.macaroon",
                cert_filepath="/path/to/your/tls.cert"
            )
        except Exception as e:
            return Response({'error': f"Error connecting to Lightning Node: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Convert amount to the appropriate data type
        try:
            amount = float(amount)
        except ValueError:
            return Response({'error': 'Invalid amount value.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Send reward sats to user's Lightning Address
            lnd.send_payment(payment_request=lightning_address, value=amount)
            return Response({'message': "Reward claimed successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f"Error sending reward: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
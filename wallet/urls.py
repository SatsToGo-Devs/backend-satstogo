from django.urls import path
from .views import WalletEndpoints

urlpatterns = [
    path('account/', WalletEndpoints.account, name='account'),
    path('receive/', WalletEndpoints.receive, name='receive'),
    path('estimate-fee/', WalletEndpoints.estimate_payment_fee, name='estimate-fee'),
]

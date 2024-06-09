from django.urls import path
from .views import WalletEndpoints, LnurlWithdrawal

urlpatterns = [
    path('account/', WalletEndpoints.account, name='account'),
    path('receive/', WalletEndpoints.receive, name='receive'),
    path('estimate-fee/', WalletEndpoints.estimate_payment_fee, name='estimate-fee'),
    path('get-withdrawal-link/', LnurlWithdrawal.get_lnurl_withdraw_link, name='get-withdrawal-link'),
    path('initiate-withdrawal/', LnurlWithdrawal.initiate_withdrawal, name='initiate-withdrawal'),
    path('confirm-withdrawal/', LnurlWithdrawal.confirm_withdrawal, name='confirm-withdrawal'),
    path('poll-withdrawal/', LnurlWithdrawal.poll_withdrawal_request, name='poll-withdrawal'),
]

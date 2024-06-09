from django.urls import path

from events.views import ActivateUser,EventCrud, RewardView, WithdrawCallbackView, RegisterUser

urlpatterns = [
    # URLS for Events
    path('register', RegisterUser.as_view(),name='register-for-event'),
    path('activate', ActivateUser.as_view(),name='activate-event'),
    path('withdraw', RewardView.as_view()),  # This is the reward endpoint
    path('callback', WithdrawCallbackView.as_view()),
    path('', EventCrud.as_view(), name='events'),
    path('export', ActivateUser.export, name='export'),
]






from django.urls import path

from events.views import ActivateUser,EventCrud, RewardView, WithdrawCallbackView

urlpatterns = [
    # URLS for Events
    path('activate', ActivateUser.as_view(),name='activate-event'),
    path('withdraw/', RewardView.as_view()),  # This is the reward endpoint
    path('callback/', WithdrawCallbackView.as_view()),
    path('', EventCrud.as_view(), name='events'),

]






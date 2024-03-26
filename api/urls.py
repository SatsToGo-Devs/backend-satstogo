from django.urls import path
from .views import RewardView, WithdrawCallbackView

urlpatterns = [
    # ... other URL patterns ...
    path('withdraw/', RewardView.as_view()),  # This is the reward endpoint
    path('callback/', WithdrawCallbackView.as_view()),
]
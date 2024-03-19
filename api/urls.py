from django.urls import path
from .views import RewardView  # Assuming RewardView is your view class

urlpatterns = [
    # ... other URL patterns ...
    path('claim-reward/', RewardView.as_view()),  # This is the reward endpoint
]

from django.urls import path
from .views import RewardView 

urlpatterns = [
    # ... other URL patterns ...
    path('withdraw/', RewardView.as_view()),  # This is the reward endpoint
]
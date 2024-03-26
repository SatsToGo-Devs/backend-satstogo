from django.urls import path
from .views import auth_view, auth_verify_view,auth_login_view

urlpatterns = [
    path('auth-verify/', auth_verify_view, name='auth-verify/'),
    path('auth-login/', auth_login_view, name='auth-login'),
    path('auth/', auth_view, name='auth'),
]
from .views import RewardView, WithdrawCallbackView

urlpatterns = [
    # ... other URL patterns ...
    path('withdraw/', RewardView.as_view()),  # This is the reward endpoint
    path('callback/', WithdrawCallbackView.as_view()),
]

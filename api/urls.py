from django.urls import path
from .views import AuthView

urlpatterns = [
    path('auth-verify/', AuthView.auth_verify_view, name='auth-verify/'),
    path('auth-login/', AuthView.auth_login_view, name='auth-login'),
    path('auth/', AuthView.auth_view, name='auth'),
]

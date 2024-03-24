from django.urls import path
from .views import login_view, get_magic_string

urlpatterns = [
    path('login/', login_view, name='login'),
    path('magic-string/', get_magic_string, name='magic-string'),
]

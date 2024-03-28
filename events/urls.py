from django.urls import path

from events.views import ActivateUser,EventCrud

urlpatterns = [
    # URLS for Events
    path('activate', ActivateUser.as_view(),name='activate-event'),
    path('', EventCrud.as_view(), name='events'),
]






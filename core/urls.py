from django.urls import path
from .views import incoming_sms, outgoing_sms, mark_sent

urlpatterns = [
    path("incoming/", incoming_sms),
    path("outgoing/", outgoing_sms),
    path("sent/", mark_sent),
]

from django.urls import path

from .views import UserAddTicket

app_name = "tickets"
urlpatterns = [
    path('report-problem/', UserAddTicket.as_view(), name='user_add_ticket')
]

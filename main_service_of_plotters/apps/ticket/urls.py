from django.urls import path

from .views import UserAddTicket, TicketListView

app_name = "tickets"
urlpatterns = [
    path('report-problem/', UserAddTicket.as_view(), name='user_add_ticket'),
    path('', TicketListView.as_view(), name='ticket_list')
]

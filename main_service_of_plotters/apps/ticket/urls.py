"""This module register url."""

from django.urls import path

from .views import (
    UserAddTicket,
    TicketListView,
    TicketDetailView,
    CloseTicketView,
    TechSpecTicketListView,
    PushTicketInWorkView,
    SolveTicketView,
)

app_name = "tickets"
urlpatterns = [
    path('report-problem/', UserAddTicket.as_view(), name='user_add_ticket'),
    path('', TicketListView.as_view(), name='ticket_list'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('<int:pk>/close/', CloseTicketView.as_view(), name='close_ticket'),
    path('solving-tickets/', TechSpecTicketListView.as_view(), name='tech_spec_list'),
    path('<int:pk>/push-in-work/', PushTicketInWorkView.as_view(), name='push_ticket_in_work'),
    path('<int:pk>/solve/', SolveTicketView.as_view(), name='solve_ticket')
]

"""This module register url."""

from django.urls import path

from .views import StatisticsPlotterView

app_name = "statistics"
urlpatterns = [
    path('statistics-plotter-list/', StatisticsPlotterView.as_view(),
         name='statistics_plotter_list'),
]

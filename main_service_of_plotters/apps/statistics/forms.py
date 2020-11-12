"""This module creates form."""

from django import forms
from main_service_of_plotters.apps.statistics.models import StatisticsPlotter


class StatisticsPlotterFrom(forms.ModelForm):
    class Meta:
        models = StatisticsPlotter
        fields = '__all__'


class StatisticsPlotterFromUserDealer(StatisticsPlotterFrom):
    class Meta:
        fields = ('plotter', 'last_request', 'count_cut', 'date_creation',)

"""This module creates form."""

from django import forms
from main_service_of_plotters.apps.statistics.models import StatisticsPlotter


class StatisticsPlotterFrom(forms.ModelForm):
    """This class create form for model StatisticsPlotter."""

    class Meta:
        """Metadata of StatisticsPlotter."""

        models = StatisticsPlotter
        fields = '__all__'


class StatisticsPlotterFromUserDealer(StatisticsPlotterFrom):
    """This class create form for model StatisticsPlotter."""

    class Meta:
        """Metadata of StatisticsPlotter."""

        fields = ('plotter', 'last_request', 'count_cut', 'date_creation',)

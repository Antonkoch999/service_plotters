"""This module create forms."""

from django import forms

from main_service_of_plotters.apps.device.models import Plotter


class PlotterForm(forms.ModelForm):
    """This class create form for model Plotter."""

    class Meta:
        model = Plotter
        fields = ('dealer', 'user', 'serial_number', )


class DealerPlotterForm(PlotterForm):
    """This class excludes field 'dealer' from model Plotter."""

    class Meta:
        exclude = ('dealer', )


class AdministratorPlotterForm(PlotterForm):
    """This class excludes field 'user' from model Plotter."""

    class Meta:
        exclude = ('user', )

"""This module create forms."""

from django import forms

from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.materials.models import Label


class PlotterForm(forms.ModelForm):
    """This class create form for model Plotter."""

    class Meta:
        model = Plotter
        fields = ('dealer', 'user', 'serial_number', 'date_creation')


class DealerPlotterForm(PlotterForm):
    """This class excludes field 'dealer' from model Plotter."""

    class Meta:
        fields = ('user', 'serial_number',)


class AdministratorPlotterForm(PlotterForm):
    """This class excludes field 'user' from model Plotter."""

    class Meta:
        fields = ('dealer', 'serial_number', )


class UserPlotterForm(PlotterForm):
    """This class excludes field 'user' from model Plotter."""

    class Meta:
        fields = ('serial_number', )


class AddLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ('scratch_code', )

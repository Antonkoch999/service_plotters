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
        exclude = ('dealer', 'date_creation')


class AdministratorPlotterForm(PlotterForm):
    """This class excludes field 'user' from model Plotter."""

    class Meta:
        exclude = ('user', 'date_creation')


class UserPlotterForm(PlotterForm):
    """This class excludes field 'user' from model Plotter."""

    class Meta:
        exclude = ('dealer', 'user', 'date_creation', 'available_film')


class AddLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ('scratch_code', )
